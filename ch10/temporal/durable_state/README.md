# Temporal durable state

This companion explains how workflow state survives worker restarts, process crashes, and long pauses.

Temporal replays the workflow history so the in-memory state can be reconstructed without losing the context needed to continue.

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
python durable_state.py
```

## Output

When you run the script, it will print the results to the terminal.
