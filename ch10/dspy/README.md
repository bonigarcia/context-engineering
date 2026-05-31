# DSPy

This Chapter 10 bucket shows how DSPy expresses a task as a signature and runs it through a module with a local deterministic LM.

## Runnable example

- `ticket_triage/`: a minimal support-ticket triage demo that assigns priority, routes to a team, and drafts a reply without external services.

## Run

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r ch10/dspy/ticket_triage/requirements.txt
   ```
3. Run the example:
   ```bash
   python ch10/dspy/ticket_triage/ticket_triage.py
   ```
