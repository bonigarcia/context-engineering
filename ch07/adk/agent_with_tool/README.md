# Agent with tool in Agent Development Kit (ADK)

This example demonstrates how to integrate and use a Python function as a tool within an ADK `LlmAgent`. The agent is configured to use a `get_current_time` function to answer questions about the current time in cities. This highlights ADK's ability to extend agent capabilities with external functionalities, thereby enriching the context available to the LLM.

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
python agent_with_tool.py
```

## Expected Output

The agent will identify the need to use the `get_current_time` tool, execute it (the mock implementation), and then respond with the time information:

```
User: What is the time in Madrid?
Agent: The time in Madrid is 10:30 AM.
```
