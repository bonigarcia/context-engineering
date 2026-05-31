# Agent with tool in Agent Development Kit (ADK)

This example demonstrates how to integrate and use a Python function as a tool within an ADK `LlmAgent`. The agent is configured to use a mock `get_current_time` function to answer questions about the current time in cities. This highlights ADK's ability to extend agent capabilities with external functionalities, thereby enriching the context available to the LLM.

## Requirements

* [Python](https://www.python.org/) 3.10+
* A [Google API key](https://ai.google.dev/) set as an environment variable (`GOOGLE_API_KEY`)

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

2. Export your API key as an environment variable:
```bash
export GOOGLE_API_KEY="sk-..." # Windows cmd: set GOOGLE_API_KEY="sk-..." # Windows PowerShell: $env:GOOGLE_API_KEY="sk-..."
```

3. Run the script:
```bash
python agent_with_tool.py
```

## Output

The agent will identify the need to use the `get_current_time` tool, execute it (the mock implementation), and then respond with the time information:

```
User: What is the time in Madrid?
Agent: The time in Madrid is 10:30 AM.
```
