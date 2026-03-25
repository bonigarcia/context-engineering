# Function calling: current time (CLI)

This example demonstrates the *function-calling loop* pattern, where the model can call external functions to get information it doesn't have. The loop is in the smallest useful form: the model decides when it needs external data, calls a function, and then uses the function result to answer.

## What you build

A tiny CLI assistant that answers: *"What time is it in X?"*

- The model can call the tool `get_current_time(city)`
- The application executes the tool deterministically (Python `zoneinfo`)
- The tool output is injected back into the conversation as a `tool` message
- The model produces the final user-facing answer grounded in the tool result

## Prerequisites

- Python 3.10+ (for `zoneinfo`)
- An OpenAI API key in `OPENAI_API_KEY`

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optional `.env` file:

```bash
OPENAI_API_KEY=your_key_here
MODEL=gpt-5
```

## Run

```bash
python function_calling.py
```

Type `/exit` to quit.

## Suggested experiment

1. Ask: `What time is it now in Paris?`
2. Ask: `What about Tokyo?`
3. Ask an unsupported city (e.g., `What time is it in Atlantis?`) and observe how the assistant handles it.

## Notes

- To extend it, add more cities or replace the tool with an API call (e.g., weather, currency rates).
