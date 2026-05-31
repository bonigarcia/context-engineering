# Stepwise reasoning with DSPy

This example shows a simple reasoned response pattern with DSPy.

It keeps the model local and deterministic, but still returns a reasoning field and a final answer field so you can see the shape of a stepwise DSPy output.

## Run

```bash
pip install -r requirements.txt
python stepwise_reasoning.py
```

## What it shows

- A DSPy signature with a reasoning field and a final answer
- A local LM stub that emits repeatable JSON
- A small offline demo with no external dependencies
