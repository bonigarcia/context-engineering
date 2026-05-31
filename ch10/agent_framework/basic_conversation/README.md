# Basic conversation with Microsoft Agent Framework

This example demonstrates how to create a basic AI agent using the Microsoft Agent Framework, configure it with system instructions, and engage in a conversation.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [OpenAI API key](https://platform.openai.com/api-keys) set as an environment variable (`OPENAI_API_KEY`)

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
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
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
