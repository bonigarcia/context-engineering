# Subagent delegation

This example does not spin up real subagents, but it documents where delegation would happen.

- One helper could select files
- One helper could summarize each file into a note
- One helper could merge the notes into `context_state`
- One helper could write the final brief

Keeping the runnable example single-file makes the control flow easier to inspect while still showing how work can be split later.

## Run

```bash
pip install -r requirements.txt
python subagent_delegation.py
```
