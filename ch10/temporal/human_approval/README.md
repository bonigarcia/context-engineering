# Temporal human approval workflow

This runnable example shows Temporal keeping an AI workflow durable while it waits for human approval.
The workflow records a draft, pauses on a signal, and then resumes when approval arrives.

## Requirements

- Python 3.10+
- A local Temporal server, such as `temporal server start-dev`

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python human_approval.py
```

## What it demonstrates

- Durable execution for long-running context flows
- Human approval as an explicit workflow signal
- State preserved across pauses and resumes
