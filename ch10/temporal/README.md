# Temporal context orchestration

This chapter shows how Temporal keeps context durable across pauses, retries, and human review.

## Examples

- `human_approval/`: a runnable workflow that drafts a response, pauses, and resumes after explicit approval
- `retry_resume/`: how a transient failure can resume without losing workflow state
- `waiting_signal/`: how a workflow waits on an external signal before continuing
- `durable_state/`: how state survives worker restarts and long pauses
- `subworkflow_boundary/`: how subworkflows keep context boundaries narrow and reusable

## Run the example

The runnable demo uses a local Temporal server.

1. Start Temporal locally:
   ```bash
   temporal server start-dev
   ```
2. Install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r ch10/temporal/human_approval/requirements.txt
   ```
3. Run the workflow worker and approval demo:
   ```bash
   python ch10/temporal/human_approval/human_approval.py
   ```
