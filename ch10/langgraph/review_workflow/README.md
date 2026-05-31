# LangGraph review workflow

This example keeps the state visible as the graph drafts an answer, reviews it, and finalizes it.

## What it demonstrates

- Explicit `draft`, `review`, and `final` state fields
- A fixed draft -> review -> finalize flow
- Intermediate state preserved in the graph output

## Run

```bash
python review_workflow.py
```
