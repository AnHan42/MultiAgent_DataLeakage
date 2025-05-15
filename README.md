# ADK-Powered medical booking tool

This project is a multi-agent AI-powered medical booking tool built using Google's Agent Development Kit (ADK). It showcases how intelligent agents can coordinate to book medical appointments while giving out first-aid advices. It simulates one agent crawling the web and interacting with a malicious website. Optionally, a Security Agent can be used to defend against data leakage. Streamlit is used for the UI, and FastAPI is used for the Agent communication and respond with structured JSON outputs.

## Workflow

This medical booking tool demonstrates a modular, orchestrated agent workflow:

User Input → Streamlit UI → Host Agent → [[Booking Agent → Security Agent], Treatment Agent]

## Getting Started

1. Clone the Repo
2. Setup Environment
3. 
```
python3 -m venv mb_demo
source mb_demo/bin/activate
pip install -r requirements.txt
```

Add your OpenAI/Gemini API key:

```
export OPENAI_API_KEY="your-api-key"
```
## Run the Agents and UI

Start agents using start_agent.bat or start_agent.sh 

Start python server: 
```
python server.py
```

Launch the frontend:
```
streamlit run booking_ui.py
```

