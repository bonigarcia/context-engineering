# Research harness

This runnable example researches a concrete repo/docs question end-to-end:

> How does this repository organize chapter 10 orchestration examples, and how does the DeepAgents slice manage context?

## What it demonstrates

- A small local file tool that only lists and reads repo/docs files
- A bounded note buffer so the harness does not carry every read forward
- A reduced `context_state` that captures only the distilled signals
- A final synthesis step that turns the reduced state into a short research brief

## Run

```bash
pip install -r requirements.txt
python research_harness.py
```
