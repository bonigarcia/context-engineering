# Stepwise reasoning with DSPy

This example shows a simple reasoned response pattern with DSPy.

It keeps the model local and deterministic, but still returns a reasoning field and a final answer field so you can see the shape of a stepwise DSPy output.

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
python stepwise_reasoning.py
```

## What it demonstrates

- A DSPy signature with a reasoning field and a final answer
- A local LM stub that emits repeatable JSON
- A small offline demo with no external dependencies

## Output

When you run the script, it will print the results to the terminal.
