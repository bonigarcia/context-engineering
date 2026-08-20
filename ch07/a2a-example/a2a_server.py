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
import random
import uuid

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)


@app.route('/agent-card.json')
def serve_agent_card():
    """Serves the agent card so that client agents can discover this agent."""
    return send_from_directory('.', 'agent-card.json')


@app.route('/message:send', methods=['POST'])
def send_message():
    """Handles a simplified A2A message:send request.

    The server reads the text parts of the incoming message, produces a mock
    forecast, and returns a completed task carrying the result as an artifact.
    """
    request_payload = request.json or {}
    message = request_payload.get("message", {})
    parts = message.get("parts", [])

    location = "an unspecified location"
    for part in parts:
        text = part.get("text", "")
        if "location:" in text.lower():
            location = text.split(":", 1)[1].strip()
            break

    # In a real implementation, the server would call an actual weather API
    # or use an internal model to generate the response
    weather = random.choice(["Sunny", "Cloudy", "Windy"])
    temperature = random.randint(30, 90)
    response_text = f"The current weather in {location} is {weather} at {temperature} degrees F."

    response_payload = {
        "task": {
            "id": str(uuid.uuid4()),
            "contextId": str(uuid.uuid4()),
            "status": {"state": "TASK_STATE_COMPLETED"},
            "artifacts": [
                {
                    "artifactId": str(uuid.uuid4()),
                    "name": "Current weather",
                    "parts": [{"text": response_text}]
                }
            ]
        }
    }
    return jsonify(response_payload), 200, {"Content-Type": "application/a2a+json"}


if __name__ == '__main__':
    print("Starting A2A Weather Agent Server...")
    print("Agent card available at http://127.0.0.1:5000/agent-card.json")
    print("Message endpoint available at http://127.0.0.1:5000/message:send")
    app.run(port=5000, debug=True)
