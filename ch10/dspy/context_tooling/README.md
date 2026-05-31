# Tool use with local context in DSPy

This example uses DSPy with a local knowledge base.

The module calls a tiny retrieval tool first, then passes the retrieved context into a `dspy.Predict` step that drafts the answer.

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
python context_tooling.py
```

## What it demonstrates

- A local tool that retrieves relevant context from an offline knowledge base
- A DSPy module that threads that context into the model call
- A repeatable local LM stub, so no external service is needed

## Output

When you run the script, it will print the results to the terminal.
