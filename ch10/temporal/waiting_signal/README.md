# Temporal waiting on a signal

This companion explains how a workflow can pause on `workflow.wait_condition(...)` until an external signal arrives.

That signal is the durable handoff point between automated work and a human or another system.

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python waiting_signal.py
```
