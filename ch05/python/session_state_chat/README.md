# Session State Chat

This example demonstrates transient session state as a structured snapshot that is updated on each turn and injected into the prompt.

It keeps track of:

- the current goal
- the current stage of the task
- lightweight constraints and open questions
- the last user and assistant messages

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
python session_state_chat.py --model gpt-5
```

## Commands

Inside the chat:

- `/help` - show commands
- `/state` - print the current session state
- `/reset` - clear the session state
- `/exit` - quit

## Suggested experiment

1. Start the chat and give it a task, for example: `Help me plan a two-day visit to Lisbon. I should keep the schedule relaxed.`
2. Ask a few follow-up questions about the task.
3. Use `/state` to inspect the live snapshot the model sees.
4. Use `/reset` and confirm that the state disappears.

## Notes

- This example is session-scoped only.
- It demonstrates local state, not durable memory.
