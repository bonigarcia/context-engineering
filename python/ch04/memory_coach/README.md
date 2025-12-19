# Memory Coach

This example accompanies Chapter 4 of *Context Engineering* and demonstrates practical memory management for an LLM-based assistant. The goal is to show, end-to-end, how an application can combine:

- Short-term memory: a sliding window of recent turns plus a rolling running summary
- Long-term semantic memory: a stable user profile stored as key/value pairs (SQLite)
- Long-term episodic memory: past events and decisions stored as embedded snippets (FAISS)

Unlike many demos that simply "store the whole chat", this example makes memory explicit:
the assistant runs a dedicated extraction step to decide what is worth persisting.

## What you build

A CLI assistant called **Memory Coach** that helps a user plan and reflect. It remembers:

- preferences that should persist (e.g., "prefers short answers", "travels in November")
- episodic events and constraints (e.g., "last time we chose Kyoto for 3 nights")

It then retrieves relevant long-term memories on each new message and injects them back into the context.

## Setup

### 1) Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure environment variables

Set an API key for the model you are using. The script uses the `openai` Python client and expects:

- `OPENAI_API_KEY` to be set
- `MODEL` (optional), default: `gpt-4.1-mini`
- `EMBEDDER` (optional), default: `sentence-transformers/all-MiniLM-L6-v2`

Example:

```bash
export OPENAI_API_KEY="..."
export MODEL="gpt-4.1-mini"
```

### 3) Run the assistant

```bash
python memory_coach.py
```

A small data directory `.memory_coach/` will be created to store SQLite files and the FAISS index.

## How to use it

Talk to the assistant normally. Use these commands to inspect memory:

- `/help` - show commands
- `/profile` - show semantic memory (stable facts/preferences)
- `/memories` - show recent episodic memories
- `/reset` - clear short-term context (window + summary)
- `/forget` - clear long-term memory (profile + episodic)
- `/exit` - quit

### Suggested experiment

1. Tell the assistant a preference (e.g., "Keep answers short and use bullet points only when necessary").
2. Discuss a small plan (e.g., "Help me plan a two-day visit to Lisbon; I like museums and walking").
3. Use `/reset` to clear short-term context and ask a follow-up question.
4. Observe that the assistant still uses your preference if it was written to the profile.
5. Use `/memories` to see which episodic details were saved.

## Project structure

- `memory_coach.py` - the CLI app
- `requirements.txt` - dependencies

## Notes

- This is a teaching example, not a hardened security design. Do not store secrets.
- If you want to adapt it for production, add explicit consent gates, PII filtering, and retention policies.
