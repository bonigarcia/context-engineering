# Temporal waiting on a signal

This companion explains how a workflow can pause on `workflow.wait_condition(...)` until an external signal arrives.

That signal is the durable handoff point between automated work and a human or another system.

## Requirements

* [Python](https://www.python.org/) 3.10+
* A [Temporal Server](https://docs.temporal.io/cli) instance running locally

## Steps for running this example in the shell

1. Install dependencies:
```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Start your local Temporal Server in a separate terminal:
```bash
temporal server start-dev
```

3. Run the script:
```bash
python waiting_signal.py
```

## Output

```
Workflow started: temporal-retry-resume-demo
The activity fails once, then Temporal retries it.
Completing activity as failed ({'activity_id': '1', 'activity_type': 'flaky_context_step', 'attempt': 1, 'namespace': 'default', 'task_queue': 'context-engineering-temporal-retry-resume', 'workflow_id': 'temporal-retry-resume-demo', 'workflow_run_id': '019e7fea-9aa9-7956-8a3f-42cf30ea473f', 'workflow_type': 'RetryResumeWorkflow'})
Traceback (most recent call last):
...
RuntimeError: transient context fetch failed
done: refined context for AI draft recovery
```
