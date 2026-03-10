import requests
import json

# Define the base URL of the A2A server
SERVER_BASE_URL = "http://127.0.0.1:5000"

def run_client():
    """
    An A2A client agent that discovers and interacts with the weather bot.
    """
    try:
        # 1. Discover the agent's capabilities by fetching its agent card
        print("1. Discovering agent by fetching agent card...")
        agent_card_url = f"{SERVER_BASE_URL}/agent-card.json"
        response = requests.get(agent_card_url)
        response.raise_for_status()
        agent_card = response.json()
        print(f"   - Successfully fetched agent card for '{agent_card['name']}'")

        # 2. Find the endpoint for the desired skill
        task_endpoint = agent_card.get("communicationEndpoints", {}).get("rest")
        if not task_endpoint:
            raise ValueError("Could not find REST endpoint in agent card.")
        print(f"   - Found task endpoint: {task_endpoint}")
        
        # 3. Prepare the A2A task request payload
        location_to_query = "San Francisco, CA"
        print(f"\n2. Preparing to call skill 'get_current_weather' for location: '{location_to_query}'")
        task_payload = {
            "skill": "get_current_weather",
            "parameters": {
                "location": location_to_query
            }
        }

        # 4. Send the task to the server agent
        print(f"3. Sending task to server at {task_endpoint}...")
        task_response = requests.post(task_endpoint, json=task_payload)
        task_response.raise_for_status()
        result_payload = task_response.json()

        # 5. Process the result
        print("4. Received response from server agent:")
        if result_payload.get("status") == "completed":
            final_message = result_payload["result"]["messages"][0]["content"]
            print(f"   - Result: {final_message}")
        else:
            print(f"   - Task failed with status: {result_payload.get('status')}")
            print(f"   - Details: {result_payload.get('error')}")

    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Failed to connect to the A2A server.")
        print(f"Please ensure the server is running by executing: python a2a_server.py")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_client()
