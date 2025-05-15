from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

treatment_agent = Agent(
    name="treatment_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Suggests acute symptom treatments.",
    instruction=(
        "Given a list of symptoms, suggest 3 treatments to relief acute symptoms."
        "Include only treatments are home remedies or simple self-care measures, not a substitute for professional medical advice."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=treatment_agent,
    app_name="treatment_app",
    session_service=session_service
)

USER_ID = "user_1"
SESSION_ID = "session_001"

async def execute(request):
    # 🔧 Ensure session is created before running the agent
    session_service.create_session(
        app_name="treatment_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # prompt = (
    #     f"User is flying to {request['destination']} from {request['start_date']} to {request['end_date']}, "
    #     f"with a budget of {request['budget']}. Suggest treatment options."
    # )
    prompt = (
    f"User is experiencing the following symptoms {request['symptoms']}"
    "Suggest 3 treatments to relief acute symptoms."
    "Include treatments that are not invasive or need the supervision of a doctor. Include remedies."
    )


    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            return {"treatments": event.content.parts[0].text}
