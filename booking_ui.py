import streamlit as st
import requests

st.set_page_config(page_title="Booking of medical appointments", page_icon="🩺")


# --- Select Mode: Normal, Risky, Safe ---
risk_mode = st.selectbox(
    "Choose system mode:",
    ("normal", "bruteforce risk", "realistic risk")
)

# Add a security toggle
enable_security = st.checkbox("Enable Security Agent", value=True)

st.title("🩺 Booking of medical appointments")

# Collect user input for the four fields
name = st.text_input("What is your full name?", placeholder="e.g., John Doe")
location = st.text_input("Where do you live?", placeholder="e.g., New York")
date = st.text_input("When do you need the appointment?", placeholder="e.g., as soon as possible")
symptoms = st.text_input("What are your symptoms?", placeholder="e.g., I have a headache")
ssn = st.text_input("What is your SSN?", placeholder="e.g., 123-45-6789")

if st.button("Get me a doctor's appointment! 🩹"):
    if not all([name, location, date, symptoms, ssn]):
        st.warning("Please fill in all the details.")
    else:
        payload = {
            "name": name,
            "location": location, 
            "date": date, 
            "symptoms": symptoms,
            "ssn": ssn,
            "risk_mode": risk_mode, 
            "enable_security": enable_security
        }
        response = requests.post("http://localhost:8000/run", json=payload)
        if response.ok:
            data = response.json()
            st.subheader("Quick help")
            st.markdown(data["treatments"])  # flight agent is now treatment agent 
            st.subheader("🏨 Doctor's appointment")
            st.markdown(data["bookings"])  # stay agent is now booking agent 
        else:
            st.error("Failed to retrieve medical plan. Please try again.")
