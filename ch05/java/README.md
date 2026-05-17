# Chapter 5 Java examples

This folder contains Java ports of the easier Chapter 5 examples.

## Requirements

- Java 21+
- Maven 3.9+
- `OPENAI_API_KEY` for the model calls
- For the Mem0 example, a running Mem0 OSS REST server and Qdrant backend

## Run

```bash
mvn compile
mvn exec:java -Dexec.mainClass="io.github.bonigarcia.ce.SessionStateChat"
mvn exec:java -Dexec.mainClass="io.github.bonigarcia.ce.WorkflowStateHandoff"
mvn exec:java -Dexec.mainClass="io.github.bonigarcia.ce.Mem0Chat"
```

## Notes

- `SessionStateChat` demonstrates transient local session state.
- `WorkflowStateHandoff` demonstrates shared state between planner and executor steps.
- `Mem0Chat` talks to a self-hosted Mem0 OSS REST server over HTTP.
- For the Mem0 example, start the server locally and point `MEM0_BASE_URL` at it (default: `http://localhost:8888`).
- If the Mem0 server requires auth, set `MEM0_API_KEY`; for a local demo you can also run the server with auth disabled.
