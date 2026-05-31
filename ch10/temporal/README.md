# Temporal context orchestration

This chapter shows how Temporal keeps context durable across pauses, retries, and human review.

## Examples

- `human_approval/`: a runnable workflow that drafts a response, pauses, and resumes after explicit approval
- `retry_resume/`: a runnable workflow that retries a transient failure without losing workflow state
- `waiting_signal/`: a runnable workflow that waits on an external signal before continuing
- `durable_state/`: a runnable workflow that survives a worker restart and resumes with state intact
- `subworkflow_boundary/`: a runnable parent/child workflow pair that keeps a narrow context boundary

## Run the examples

The demos use a local Temporal server.

1. Start Temporal locally:
   ```bash
   temporal server start-dev
   ```
2. Install dependencies for the companion you want to run:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r ch10/temporal/<companion>/requirements.txt
   ```
3. Run one of the workflows:
   ```bash
   python ch10/temporal/<companion>/<companion>.py
   ```
