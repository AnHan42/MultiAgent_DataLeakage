#!/bin/bash

gnome-terminal -- bash -c "uvicorn agents.host_agent.__main__:app --port 8000; exec bash"
gnome-terminal -- bash -c "uvicorn agents.treatment_agent.__main__:app --port 8001; exec bash"
gnome-terminal -- bash -c "uvicorn agents.booking_agent.__main__:app --port 8002; exec bash"
gnome-terminal -- bash -c "uvicorn agents.security_agent.__main__:app --port 8003; exec bash"