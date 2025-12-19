# Session Memory

This example accompanies Chapter 4 of *Context Engineering* and demonstrates **short-term memory**
management using the OpenAI Agents SDK `Session` abstraction. It includes two strategies:

- `TrimmingSession`: keeps only the last *N* user turns (deterministic, no extra model calls)
- `SummarizingSession`: keeps the last *N* turns verbatim and compresses older turns into a running summary
  (preserves long-range constraints at the cost of occasional extra calls)

## Prerequisites

- Python 3.10+
- An OpenAI API key (`OPENAI_API_KEY`)

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Optional `.env` file:

```bash
OPENAI_API_KEY=your_key_here
MODEL=gpt-5
MAX_TURNS=8
REFRESH_EVERY=4
SESSION_ID=support_demo
```

## Run

### Trimming strategy (fast, deterministic)

```bash
python session_memory_chat.py --strategy trim --max-turns 6
```

### Summarization strategy (better long-range continuity)

```bash
python session_memory_chat.py --strategy summarize --max-turns 6 --refresh-every 3
```

## Commands

Inside the chat:

- `/help` – show commands
- `/state` – print the *current session state* (what the agent will see on the next turn)
- `/reset` – clear the session
- `/exit` – quit

## Suggested experiment

1. Start with `--strategy trim --max-turns 3`.
2. Describe two separate issues (e.g., "Wi-Fi drops every hour" and "printer won't connect").
3. Continue chatting until the first issue scrolls out of the last 3 user turns.
4. Observe that the agent begins to lose the earlier constraint (expected with trimming).
5. Repeat with `--strategy summarize` and note that older constraints survive in the running summary.

## Notes

- This example demonstrates **session-scoped memory**, not cross-session persistence.
- For durable memory across sessions, combine Sessions with a long-term store (e.g., Mem0 + Qdrant).
