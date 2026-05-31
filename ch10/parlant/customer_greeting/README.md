# Parlant customer greeting guideline

This example shows Parlant loading only the relevant conversational context for a greeting.
The agent is created with one guideline, so the response changes only when the customer actually greets it.

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
python customer_greeting.py
```

## What it demonstrates

* A real Parlant agent
* One guideline selected by conversational context
* A lightweight harness instead of a graph or workflow engine

## Output

When you run the script, it will print the results to the terminal.
