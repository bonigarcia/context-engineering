# Session Memory

This example accompanies Chapter 4 of *Context Engineering* and demonstrates short-term memory
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

## Suggested experiment: The Secret Code

This experiment will give the agent a secret code, distract it with unrelated conversation, and then see if it can recall the code with each strategy.

### Part 1: The `trim` Strategy (The Forgetful Agent)

1.  Start the chat with `trim` and a very short memory of only 2 turns:
    ```bash
    python session_memory_chat.py --strategy trim --max-turns 2
    ```

2.  Give it the secret. At the first prompt, type:
    > `My name is Alex and the secret code is 'blue-banana-boat'. Please remember this.`

3.  Distract the agent. Now, have a short, unrelated conversation to push the secret code out of its memory. Send these two messages, one after the other:
    > `What is the capital of Spain?`

    > `What is the most popular sport there?`

4.  Test its memory. Ask for the code back:
    > `What was the secret code I told you earlier?`

Expected Outcome: The agent will fail. Because `max-turns` was 2, it only remembers the last two things you talked about (France and sports). The secret code is forgotten.

### Part 2: The `summarize` Strategy (The Remembering Agent)

1.  Restart the chat with the `summarize` strategy. We'll tell it to summarize after every 2 turns.
    ```bash
    python session_memory_chat.py --strategy summarize --max-turns 2 --refresh-every 2
    ```

2.  Repeat the process. Have the exact same conversation as before:
    > `My name is Alex and the secret code is 'blue-banana-boat'. Please remember this.`

    > `What is the capital of Spain?`

    > `What is the most popular sport there?`

3.  Test its memory again.
    > `What was the secret code I told you earlier?`

Expected Outcome: The agent will succeed. Even though the secret code was pushed out of the immediate 2-turn memory, the `summarize` strategy created a summary in the background (e.g., "User is Alex, secret code is blue-banana-boat"). This summary is included in the context, allowing the agent to recall the code correctly.

## Notes

- This example demonstrates session-scoped memory, not cross-session persistence.
- For durable memory across sessions, combine Sessions with a long-term store (e.g., Mem0 + Qdrant).
