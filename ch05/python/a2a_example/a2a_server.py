import json
from flask import Flask, jsonify, request, send_from_directory
import random
import uuid

app = Flask(__name__)

@app.route('/agent-card.json')
def serve_agent_card():
    """Serves the agent-card.json file for discovery."""
    return send_from_directory('.', 'agent-card.json')

@app.route('/tasks', methods=['POST'])
def handle_task():
    """Handles incoming A2A tasks."""
    task_data = request.json
    
    # Basic validation of the incoming task
    if not task_data or 'skill' not in task_data or 'parameters' not in task_data:
        return jsonify({"error": "Invalid task format"}), 400

    skill_name = task_data['skill']
    parameters = task_data['parameters']

    if skill_name == 'get_current_weather':
        location = parameters.get('location', 'an unspecified location')
        
        # --- In a real agent, this is where you'd call a weather API ---
        # For this example, we'll just return a mock response.
        mock_conditions = ["Sunny", "Cloudy with a chance of rain", "Windy", "Snowing"]
        temperature = random.randint(30, 90)
        weather = random.choice(mock_conditions)
        
        response_text = f"The current weather in {location} is {weather} at {temperature}°F."
        
        # Construct an A2A-compliant response
        response_payload = {
            "taskId": str(uuid.uuid4()),
            "status": "completed",
            "result": {
                "messages": [
                    {
                        "role": "agent",
                        "content": response_text
                    }
                ]
            }
        }
        return jsonify(response_payload)
    else:
        return jsonify({"error": f"Skill '{skill_name}' not supported"}), 404

if __name__ == '__main__':
    # In a real scenario, you might want to specify the host and port
    # For simplicity, we run on the default 127.0.0.1:5000
    print("Starting A2A Weather Agent Server...")
    print("Agent Card available at http://127.0.0.1:5000/agent-card.json")
    print("Task endpoint available at http://127.0.0.1:5000/tasks")
    app.run(port=5000, debug=True)
