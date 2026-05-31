# Temporal subworkflow boundary

This companion explains how a subworkflow can keep a narrow context boundary around one durable step.

Use it when a larger flow needs reusable orchestration logic without exposing every internal detail to the parent workflow.

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python subworkflow_boundary.py
```
