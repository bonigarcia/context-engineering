# Code Review Agent with Amazon Bedrock AgentCore

This example wraps a code review agent in the entrypoint that [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) Runtime expects. The agent accepts a code diff and returns structured review feedback covering correctness, security, maintainability, and style.

The AgentCore runtime provides session isolation, identity, and observability, so the agent code only declares how a request becomes a response.

## Requirements

- [Python](https://www.python.org/) 3.10+
- AWS credentials configured for a region where Amazon Bedrock is available
- Model access granted for the model identifier used in the script

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
python code_review_agent.py
```

3. Send a diff to the local endpoint:
```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d "{\"diff\": \"@@ -0,0 +1,9 @@\n+import os\n+\n+def get_api_key():\n+    return os.environ['API_KEY']\n+\n+def process(data):\n+    exec(data)\n+    return 'done'\n\"}"
```

## Output

The local server answers on `/invocations` with a structured JSON review. The same entrypoint is what AgentCore Runtime invokes once deployed, so no code changes are needed between local runs and the managed runtime. This pattern turns any review checklist into a deployable code review service.