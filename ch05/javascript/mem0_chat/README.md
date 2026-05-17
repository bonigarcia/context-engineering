# Memory-backed chat

This example demonstrates a practical Mem0-backed memory stack in JavaScript.

## Requirements

- Node.js 18+
- An OpenAI API key in `OPENAI_API_KEY`
- A running Qdrant instance for Mem0 (`localhost:6333` by default)

## Environment

- `MODEL` - OpenAI model to use (default: `gpt-5`)
- `USER_ID` - user scope for memory storage (default: `alice`)
- `MEM0_COLLECTION` - Qdrant collection name (default: `context_engineering_demo`)
- `QDRANT_HOST` / `QDRANT_PORT` - Qdrant connection settings

## Start Qdrant

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

## Install

```bash
npm install
```

## Run

```bash
npm start
```

## Commands

- `/help` - show commands
- `/memories` - show stored memories for the user
- `/forget` - delete stored memories for the user
- `/exit` - quit
