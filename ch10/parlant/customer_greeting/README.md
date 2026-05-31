# Parlant customer greeting guideline

This example shows Parlant loading only the relevant conversational context for a greeting.
The agent is created with one guideline, so the response changes only when the customer actually greets it.

## Requirements

* Python 3.10+
* `parlant`
* An `OPENAI_API_KEY` environment variable

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python customer_greeting.py
```

While the script is running, open `http://localhost:8800` in the Parlant UI, start a session with the agent, and greet it to trigger the guideline.

## What it demonstrates

* A real Parlant agent
* One guideline selected by conversational context
* A lightweight harness instead of a graph or workflow engine
