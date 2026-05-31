# Temporal subworkflow boundary

This companion explains how a subworkflow can keep a narrow context boundary around one durable step.

Use it when a larger flow needs reusable orchestration logic without exposing every internal detail to the parent workflow.

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
python subworkflow_boundary.py
```

## Output

When you run the script, it will print the results to the terminal.
