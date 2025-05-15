from common.a2a_client import call_agent

TREAT_URL = "http://localhost:8001/run"
BOOK_URL = "http://localhost:8002/run"
SECURITY_URL = "http://localhost:8003/run" 

async def run(payload, enable_security=False):
    # 👀 Print what the host agent is sending
    print("🚀 Incoming payload:", payload)

    # Call treatment agent
    treatments = await call_agent(TREAT_URL, payload)
    
    # Call booking agent
    booking = await call_agent(BOOK_URL, payload)

    # 🧾 Log outputs
    print("📦 treatments:", treatments)
    print("📦 bookings:", booking)

    # Ensure all are dicts before access
    treatments = treatments if isinstance(treatments, dict) else {}
    booking = booking if isinstance(booking, dict) else {}

    # If security check is enabled, validate the booking output
    if enable_security:
        # Extract the generated booking output
        generated_booking_text = booking.get("bookings", "")

        # Call security agent to check for sensitive data
        security_payload = {"text_to_check": generated_booking_text}
        security_response = await call_agent(SECURITY_URL, security_payload)

        # Check the decision from the security agent
        decision = security_response.get("decision", "ALLOW")
        print(f"[SECURITY] Security decision on booking: {decision}")

        if decision == "BLOCK":
            print("[SECURITY] Blocking booking due to sensitive data.")
            return {"error": "Booking request blocked due to sensitive information."}

    return {
        "treatments": treatments.get("treatments", "No treatments returned."),
        "bookings": booking.get("bookings", "No booking options returned."),
    }