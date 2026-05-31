# Pipeline composition

This example composes a small Haystack pipeline out of separate retrieval, context assembly, and response formatting stages.

## Requirements

- Python 3.10+
- `haystack-ai`

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python haystack_pipeline_composition.py
```

The example shows how each stage has one job, making the flow easy to read and reuse.
