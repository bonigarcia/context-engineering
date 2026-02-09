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
   Ensure your Google API key (`GOOGLE_API_KEY`) is set as an environment variable.

3. Run the script:
```bash
python basic_agent.py
```

## Expected Output

The agent will respond to user prompts, for example as follows:

```
User: Hello, agent!
Agent: Hello there! How can I assist you today?
```