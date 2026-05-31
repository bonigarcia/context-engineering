# Tool use with local context in DSPy

This example uses DSPy with a local knowledge base.

The module calls a tiny retrieval tool first, then passes the retrieved context into a `dspy.Predict` step that drafts the answer.

## Run

```bash
pip install -r requirements.txt
python context_tooling.py
```

## What it shows

- A local tool that retrieves relevant context from an offline knowledge base
- A DSPy module that threads that context into the model call
- A repeatable local LM stub, so no external service is needed
