from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- Define security agent ---
security_agent = Agent(
    name="security_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Monitors and blocks sensitive data leakage.",
    instruction=(
        "You are a strict security checker.\n"
        "If the text includes sensitive personal information like SSN, credit card numbers, or full birth dates,\n"
        "respond exactly 'BLOCK'.\n"
        "Otherwise, respond exactly 'ALLOW'."
    )
)


session_service = InMemorySessionService()
runner = Runner(
    agent=security_agent,
    app_name="security_app",
    session_service=session_service
)


USER_ID = "user_3"
SESSION_ID = "session_003"


async def execute(request):
    # Ensure session is created before running the agent
    session_service.create_session(
        app_name="security_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    text_to_check = request.get("text_to_check", "")  # Get the text we want to analyze

    prompt = (
        f"Analyze the following text for sensitive personal data:\n\n"
        f"{text_to_check}\n\n"
        f"Remember: If sensitive information is present, respond exactly 'BLOCK'. Otherwise, respond 'ALLOW'."
    )

    print("[SECURITY] Starting security check for the generated text.")

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            decision = event.content.parts[0].text.strip().upper()  # ensure it's clean
            print(f"[SECURITY] Decision received: {decision}")
            if decision not in ["BLOCK", "ALLOW"]:
                decision = "ALLOW"  # fallback

            return {"decision": decision}