from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

host_agent = Agent(
    name="host_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Coordinates medical help by calling treatment and booking agents.",
    instruction="You are the host agent responsible for orchestrating medical help tasks. "
                "You call external agents to gather acute symptom treatments and details on booking a doctor's appointment, then return a final result."
)

session_service = InMemorySessionService()
runner = Runner(
    agent=host_agent,
    app_name="host_app",
    session_service=session_service
)

USER_ID = "user_host"
SESSION_ID = "session_host"

async def execute(request):
    # Ensure session exists
    session_service.create_session(
        app_name="host_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    prompt = (
        f"Suggest symptomatic treatments to relief the symptoms {request['symptoms']}. Point out that those treatments are only home remedies or simple self-care measures, not a substitute for professional medical advice."
        f"Suggest the right doctor. Simulate the booking of a doctor's appointment for the date requests {request['date']}."
        f"Call the treatment and booking agents for results and optionally let the security agent check bookings agents output."
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            return {"summary": event.content.parts[0].text}
