# Workflow State Handoff

This example demonstrates shared workflow state in a basic two-agent system.

It uses:

- a planner agent that writes the objective, plan, and handoff note
- an executor agent that reads the same shared state and advances the workflow
- a JSON file so the state survives across runs

## Prerequisites

- Python 3.10+
- An OpenAI API key (`OPENAI_API_KEY`)

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```bash
python workflow_state_handoff.py --model gpt-5
```

By default, the shared state is stored in `.workflow_state_handoff.json`.

## Commands

Inside the chat:

- `/help` - show commands
- `/state` - print the shared workflow state
- `/reset` - clear the workflow state file
- `/exit` - quit

## Suggested experiment

1. Start the script and give it a concrete task, for example: `Plan a launch checklist for a small product demo.`
2. Observe the planner output and the executor output.
3. Run `/state` to inspect the shared state that both agents use.
4. Restart the script and confirm that the plan is still available from the state file.

## Notes

- This example demonstrates global/shared state.
- It is intentionally minimal and focuses on the state handoff, not on tool use or distributed coordination.
