@echo off

start cmd /k uvicorn agents.host_agent.__main__:app --port 8000
start cmd /k uvicorn agents.treatment_agent.__main__:app --port 8001
start cmd /k uvicorn agents.booking_agent.__main__:app --port 8002
start cmd /k uvicorn agents.security_agent.__main__:app --port 8003
