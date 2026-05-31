# Temporal retry and resume

This companion explains the pattern where a transient failure interrupts an AI step, then Temporal retries it and resumes from durable workflow state.

The key idea is that the workflow keeps its progress in Temporal, so a retry does not rebuild the full context from scratch.

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
python retry_resume.py
```

## Output

When you run the script, it will print the results to the terminal.
