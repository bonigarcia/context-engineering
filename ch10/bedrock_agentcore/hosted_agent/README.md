# Hosted agent with Amazon Bedrock AgentCore

This example wraps an agent in the entrypoint that [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) Runtime expects. The service supplies the runtime around the agent, including session isolation, identity, and observability, so the code only declares how a request becomes a response.

## Requirements

* [Python](https://www.python.org/) 3.10+
* AWS credentials configured for a region where Amazon Bedrock is available
* Model access granted for the model identifier used in the script

## Steps for running this example in the shell

1. Install dependencies:
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

2. Run the agent locally:
```bash
python hosted_agent.py
```

3. Send a request to the local endpoint:
```bash
curl -X POST http://localhost:8080/invocations -H "Content-Type: application/json" -d "{\"prompt\": \"Explain context engineering in one sentence.\"}"
```

## Output

The local server answers on `/invocations` with the model reply wrapped in a `result` field. The same entrypoint is what AgentCore Runtime invokes once the agent is deployed, so no code changes are needed between local runs and the managed runtime.
