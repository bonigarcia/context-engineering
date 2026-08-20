"""
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import uuid

import requests

# Base URL of the A2A server agent
SERVER_BASE_URL = "http://127.0.0.1:5000"


def run_client():
    """An A2A client agent that discovers and interacts with the weather bot."""
    try:
        # 1. Discover the server agent by fetching its agent card
        print("1. Discovering agent by fetching agent card...")
        agent_card_url = f"{SERVER_BASE_URL}/agent-card.json"
        response = requests.get(agent_card_url)
        response.raise_for_status()
        agent_card = response.json()
        print(f"   - Fetched agent card for '{agent_card['name']}'")

        # 2. Select a supported interface declared in the agent card
        interfaces = agent_card.get("supportedInterfaces", [])
        if not interfaces:
            raise ValueError("Agent card does not declare a supported interface.")
        message_endpoint = interfaces[0]["url"]
        print(f"   - Selected message endpoint: {message_endpoint}")

        # 3. Build a minimal A2A message payload
        location_to_query = "San Francisco, CA"
        print(f"\n2. Requesting the current weather for '{location_to_query}'")
        message_payload = {
            "message": {
                "messageId": str(uuid.uuid4()),
                "role": "ROLE_USER",
                "parts": [{"text": f"Current weather. location: {location_to_query}"}]
            },
            "configuration": {"acceptedOutputModes": ["text/plain"]}
        }

        # 4. Send the message to the server agent
        print(f"3. Sending message to {message_endpoint}...")
        headers = {"Content-Type": "application/a2a+json"}
        message_response = requests.post(message_endpoint, json=message_payload, headers=headers)
        message_response.raise_for_status()
        result_payload = message_response.json()

        # 5. Read the artifact returned by the completed task
        print("4. Received response from the server agent:")
        task = result_payload.get("task", {})
        state = task.get("status", {}).get("state")
        if state == "TASK_STATE_COMPLETED":
            artifact = task["artifacts"][0]
            final_message = artifact["parts"][0]["text"]
            print(f"   - Result: {final_message}")
        else:
            print(f"   - Task did not complete. State: {state}")

    except requests.exceptions.RequestException as e:
        print("\n[ERROR] Failed to connect to the A2A server.")
        print("Please ensure the server is running by executing: python a2a_server.py")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_client()
