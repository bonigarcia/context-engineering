# Agent-to-Agent (A2A) communication example

This example provides a hands-on demonstration of the **Agent-to-Agent (A2A)** protocol. It includes a simple server agent (a "weather bot") and a client agent that discovers and interacts with it.

The demonstration covers the core concepts of A2A:
1. Agent card discovery: The client fetches an `agent-card.json` file from a well-known endpoint to learn the server's identity, capabilities, skills, and supported interfaces.
2. Message-based communication: The client sends a message made of parts to the `message:send` endpoint declared in the agent card.
3. Task-shaped responses: The server replies with a completed task that carries the result as an artifact.
4. Client-server interaction: A clear and simple showcase of two Python processes acting as distinct agents communicating over HTTP.

This code is a teaching scaffold, not a conformant implementation. It omits authentication, signed agent cards, full capability validation, streaming, push notifications, polling, version negotiation, and the complete error model. Consult the [A2A specification](https://a2a-protocol.org/) before building a production agent.

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

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

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

The client performs discovery and message submission automatically, printing its progress to the console. You will see it fetch the agent card, select the supported interface, send the message, and display the weather information carried in the artifact of the completed task:

```
1. Discovering agent by fetching agent card...
   - Fetched agent card for 'Nimbus Weather Bot'
   - Selected message endpoint: http://127.0.0.1:5000/message:send

2. Requesting the current weather for 'San Francisco, CA'
3. Sending message to http://127.0.0.1:5000/message:send...
4. Received response from the server agent:
   - Result: The current weather in San Francisco, CA is Sunny at 51 degrees F.
```
