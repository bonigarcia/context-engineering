# Parlant guideline routing

This companion explains how Parlant keeps multiple behavioral rules narrow by matching only the guideline that fits the current turn.

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python guideline_routing.py
```

## What it demonstrates

* Context-selected guidance instead of a monolithic prompt
* Rule matching based on the current conversation
* Less irrelevant instruction noise in the active context window
