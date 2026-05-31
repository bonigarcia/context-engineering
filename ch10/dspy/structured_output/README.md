# Structured output with DSPy

This example uses DSPy with a local deterministic LM to turn a request into a small structured action plan.

## Run

```bash
pip install -r requirements.txt
python structured_output.py
```

## What it shows

- A DSPy signature with typed outputs
- A local LM stub that emits repeatable JSON
- A `dspy.Predict` module that parses the plan fields
