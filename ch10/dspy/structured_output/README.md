# Structured output with DSPy

This example uses DSPy with a local deterministic LM to turn a request into a small structured action plan.

## Requirements

* [Python](https://www.python.org/) 3.10+

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

2. Run the script:
```bash
python structured_output.py
```

## What it demonstrates

- A DSPy signature with typed outputs
- A local LM stub that emits repeatable JSON
- A `dspy.Predict` module that parses the plan fields

## Output

When you run the script, it will print the results to the terminal.
