# Agent-to-Agent (A2A) communication example

This example provides a hands-on demonstration of the **Agent-to-Agent (A2A)** protocol. It includes a simple server agent (a "weather bot") and a client agent that discovers and interacts with it.

The demonstration covers the core concepts of A2A:
1. Agent card discovery: The client fetches a `agent-card.json` file from a well-known endpoint to learn about the server's capabilities.
2. Task-based communication: The client sends a structured request to the server's task endpoint to execute a skill.
3. Client-server Interaction: A clear and simple showcase of two Python processes acting as distinct agents communicating over HTTP.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the following libraries:

* Flask: A micro web framework for the server agent.
* Requests: A library for making HTTP requests from the client agent.

All dependencies are listed in `requirements.txt` and can be installed from there.

## Steps for running this example

This example requires two separate terminal sessions.

### 1. Start the A2A server agent

In your first terminal, navigate to this source directory and run the server:

* Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

* Run the server:
```bash
flask --app a2a_server run
```

The server will start and print messages indicating it's running, usually on `http://127.0.0.1:5000`. Keep this terminal open.

### 2. Run the A2A client agent

In your second terminal, navigate to the same directory.

* Run the client:
```bash
python a2a_client.py
```

## Output

The client will automatically perform the discovery and task execution steps, printing its progress to the console. You will see it fetch the agent card, find the task endpoint, send the request, and display the weather information returned by the server.