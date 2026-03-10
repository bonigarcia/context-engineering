# Basic conversation with Microsoft Agent Framework

This example demonstrates how to create a basic AI agent using the Microsoft Agent Framework, configure it with system instructions, and engage in a conversation.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Setup

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
   Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

3. Run the script:
```bash
python basic_conversation.py
```

## Output

The script will output the agent's response:

```
User: What is the size of your context window
Agent response: I don’t have a way to see the exact limit for your setup, but most current deployments of me run with a 128,000‑token context window (roughly ~100k words). If you can tell me the exact model name you’re using here, I can confirm the precise limit.
```
