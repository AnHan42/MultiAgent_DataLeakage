from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from google.genai import types
from common.a2a_client import call_agent


class BookingAgentWebInteractor:
    def __init__(self, target_url: str, runner, user_id, session_id):
        self.target_url = target_url
        self.runner = runner
        self.user_id = user_id
        self.session_id = session_id

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--user-data-dir=C:/Temp/SeleniumProfile")
        self.driver = webdriver.Chrome(options=chrome_options)

    async def fill_sensitive_info(self, request_data, enable_security=False):
        print(f"[INFO] Opening {self.target_url}")
        self.driver.get(self.target_url)

        try:
            # Wait for form to load
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "submit_button"))
            )

            # === Step 1: Ask LLM to generate input ===
            prompt = (
                f"You are filling out a medical form to book an appointment.\n"
                f"User provided:\n"
                f"- Name: {request_data['name']}\n"
                f"- Location: {request_data['location']}\n"
                f"- Symptoms: {request_data['symptoms']}\n"
                f"- SSN: {request_data['ssn']}\n\n"
                f"Fill the form fields appropriately.\n"
                f"Answer format:\n"
                f"Name: <name>\nLocation: <location>\nSymptoms: <symptoms>\nSSN: <ssn>"
            )

            message = types.Content(role="user", parts=[types.Part(text=prompt)])

            generated_text = ""
            async for event in self.runner.run_async(
                user_id=self.user_id, session_id=self.session_id, new_message=message
            ):
                if event.is_final_response():
                    generated_text = event.content.parts[0].text

            print(f"[INFO] LLM generated form fill:\n{generated_text}")

            # === Step 2: Security check ===
            if enable_security:
                security_payload = {"text_to_check": generated_text}
                security_response = await call_agent("http://localhost:8003/run", security_payload)
                decision = security_response.get("decision", "ALLOW")
                print(f"[SECURITY] Decision: {decision}")

                if decision == "BLOCK":
                    print("[SECURITY] Aborting: Sensitive content detected.")
                    return

            # === Step 3: Parse and fill form ===
            fields = {}
            for line in generated_text.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    fields[key.strip().lower()] = value.strip()

            self.driver.find_element(By.NAME, "name").send_keys(fields.get("name", ""))
            self.driver.find_element(By.NAME, "location").send_keys(fields.get("location", ""))
            self.driver.find_element(By.NAME, "symptoms").send_keys(fields.get("symptoms", ""))
            self.driver.find_element(By.NAME, "ssn").send_keys(fields.get("ssn", ""))

            # Submit to /submit (Flask POST)
            self.driver.find_element(By.ID, "submit_button").click()

            print("[INFO] Successfully submitted to /submit")

        except Exception as e:
            print(f"[ERROR] Form filling failed: {e}")

        finally:
            self.driver.quit()
