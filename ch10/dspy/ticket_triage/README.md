# Ticket triage

This example uses DSPy with a local deterministic LM to classify a support ticket, assign a team, and draft a short reply.

## Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python ticket_triage.py
   ```

## What it shows

- A DSPy signature for structured ticket triage
- A local LM stub that returns repeatable JSON
- A `dspy.Predict` module that parses the JSON into typed outputs
