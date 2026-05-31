# Temporal durable state

This companion explains how workflow state survives worker restarts, process crashes, and long pauses.

Temporal replays the workflow history so the in-memory state can be reconstructed without losing the context needed to continue.

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python durable_state.py
```
