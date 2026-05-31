# Temporal human approval workflow

This runnable example shows Temporal keeping an AI workflow durable while it waits for human approval.
The workflow records a draft, pauses on a signal, and then resumes when approval arrives.

## Requirements

* [Python](https://www.python.org/) 3.10+
* A [Temporal Server](https://docs.temporal.io/cli) instance running locally

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

2. Start your local Temporal Server in a separate terminal:
```bash
temporal server start-dev
```

3. Run the script:
```bash
python human_approval.py
```

## What it demonstrates

- Durable execution for long-running context flows
- Human approval as an explicit workflow signal
- State preserved across pauses and resumes

## Output

```
Workflow started: temporal-human-approval-demo
The workflow is paused until you approve it.
Press Enter to approve and resume...
Draft response for release note for a customer escalation: keep the answer concise and context-aware. Approved by human reviewer.
```
