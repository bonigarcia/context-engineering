# LangGraph checkpointed resume

This example shows persisted state surviving a pause/resume boundary.

## What it demonstrates

- A graph compiled with a checkpointer
- State loaded back by thread id after the first pause
- Final state completed on resume without losing the draft

## Run

```bash
python checkpointed_resume.py
```
