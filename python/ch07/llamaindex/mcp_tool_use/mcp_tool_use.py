import os
import threading
import time
from dotenv import load_dotenv
from flask import Flask, jsonify
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llama_index.tools.mcp import BasicMCPClient
from llama_index.tools.mcp.utils import mcp_tool_from_spec

# Load environment variables from .env file
load_dotenv()

# Check if OPENAI_API_KEY is set
if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# --- 1. Define a simple Flask app to simulate an MCP server ---
app = Flask(__name__)

# This would be a more complex MCP spec in a real scenario
# For simplicity, we define a basic structure here.
@app.route("/.well-known/mcp", methods=["GET"])
def get_mcp_spec():
    return jsonify({
        "mcp_version": "0.1.0",
        "name": "dummy_mcp_service",
        "description": "A dummy MCP service for demonstration.",
        "tools": [
            {
                "name": "get_dummy_data",
                "description": "Retrieves some dummy data from the service.",
                "input_schema": {"type": "object", "properties": {}},
                "output_schema": {"type": "object", "properties": {"data": {"type": "string"}}},
                "api_endpoint": "/dummy_data",
                "http_method": "GET"
            }
        ]
    })

@app.route("/dummy_data", methods=["GET"])
def get_dummy_data():
    return jsonify({"data": "This is some dummy data from the MCP service."})

def run_flask_app():
    # Use a specific port to avoid conflicts
    app.run(port=5001, debug=False, use_reloader=False)

# --- Main execution ---
if __name__ == "__main__":
    print("Starting dummy MCP server in a background thread...")
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True # Allow the main program to exit even if thread is running
    flask_thread.start()
    time.sleep(2) # Give the server a moment to start

    mcp_server_url = "http://localhost:5001"
    print(f"Dummy MCP server running at: {mcp_server_url}")

    # 2. Use BasicMCPClient to convert the simulated MCP server into a LlamaIndex tool
    # First, get the MCP spec
    try:
        mcp_client = BasicMCPClient(mcp_server_url)
        mcp_spec = mcp_client.get_mcp_spec()
        print("Successfully fetched MCP spec.")
    except Exception as e:
        print(f"Error fetching MCP spec: {e}")
        print("Ensure the Flask app started successfully and is accessible.")
        exit(1)

    # Convert the MCP tools to LlamaIndex tools
    llama_tools = []
    for tool_spec in mcp_spec["tools"]:
        llama_tool = mcp_tool_from_spec(tool_spec, mcp_client)
        llama_tools.append(llama_tool)

    # 3. Initialize an OpenAIAgent with this MCP tool
    llm = OpenAI(model="gpt-4o") # Using a more capable model for better agent reasoning

    agent = OpenAIAgent.from_tools(
        tools=llama_tools,
        llm=llm,
        verbose=True,
    )

    # 4. Demonstrate an interaction where the agent uses the MCP tool
    print("--- Interaction 1: Question requiring the MCP tool ---")
    response = agent.chat("Can you get me some dummy data?")
    print(f"Agent: {response}")

    print("--- Interaction 2: General question (should not use MCP tool) ---")
    response = agent.chat("What is the capital of Spain?")
    print(f"Agent: {response}")

    print("MCP tool use example finished. The dummy Flask server might still be running in the background until the process exits.")
