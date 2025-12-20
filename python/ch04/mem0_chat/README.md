# Memory-backed chat

This example accompanies Chapter 4 of *Context Engineering* and demonstrates a practical memory stack:

- OpenAI GPT-5 is used as LLM.
- Mem0 stores and retrieves long-term memories extracted from the conversation.
- Qdrant is the vector database backend used by Mem0 for semantic retrieval.

The key takeaway is architectural: GPT-5 remains stateless between runs, while Mem0+Qdrant provides durable, searchable memory that can be injected back into the model’s context on each turn.

## What you build

A CLI chat application that:
1. Retrieves relevant long-term memories from Mem0/Qdrant for each user message
2. Passes those memories to GPT-5 as part of the system instructions
3. Stores the latest interaction back into Mem0 so it can influence future sessions

## Prerequisites

- Python 3.10+
- An OpenAI API key (export `OPENAI_API_KEY`)
- A running Qdrant instance (local Docker is easiest)

## Start Qdrant locally (Docker)

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

Qdrant will listen on `localhost:6333` by default.

If you already run Qdrant elsewhere, set:
- `QDRANT_HOST`
- `QDRANT_PORT`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (optional):

```bash
OPENAI_API_KEY=your_key_here
MODEL=gpt-5
QDRANT_HOST=localhost
QDRANT_PORT=6333
MEM0_COLLECTION=context_engineering_demo
```

## Run

```bash
python mem0_chat.py --user alice
```

## Commands

Inside the chat:

- `/help` – show commands
- `/memories` – show a sample of stored memories for the user (best-effort)
- `/forget` – clear stored memories for the user (best-effort)
- `/exit` – quit

## Suggested experiment

1. Tell the assistant a stable preference (e.g., "When I ask for recommendations, I prefer a short list with pros/cons.").
2. Exit the program and run it again.
3. Ask a related question ("Recommend books for my next trip.").
4. Observe that the assistant recalls and applies your preference, even though the in-session transcript is empty.
5. Run `/memories` to inspect what was stored.

## Notes

- Mem0 performs extraction and conflict resolution when adding memories (default behavior).
- The script keeps a small in-session transcript (`--window`) for local coherence; cross-session continuity comes from Mem0+Qdrant.
