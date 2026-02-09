# Basic agent with Agent Development Kit (ADK)

This example demonstrates how to create and run a simple LLM agent using the Agent Development Kit (ADK). The agent is configured with a basic system instruction and responds to a user prompt, showcasing the fundamental interaction flow in ADK.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
   Ensure your Google API key is set as an environment variable. You can do this by:
```
echo 'GOOGLE_API_KEY="YOUR_API_KEY"' > my_agent/.env
```

3. Run the script:
```bash
adk run my_agent
```

## Expected Output

The agent will respond to user prompts, for example as follows:

```
--- Starting conversation with hello-agent ---
User: Hello, agent!
Agent: Hello there! How can I help you today?
--- Conversation ended ---
```
