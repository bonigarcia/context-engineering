# Retrieval with Spring AI and Ollama

This example shows a tiny local RAG flow using Spring AI, Ollama embeddings, and an in-memory vector store.

It indexes a few short notes, retrieves the best match, and asks the chat model to answer from that context.

## Requirements

- Java 21+
- Maven 3.9+
- Ollama running locally on `http://localhost:11434`
- A pulled chat model such as `llama3.2:1b`
- A pulled embedding model such as `nomic-embed-text`

## Run

```bash
ollama serve
ollama pull llama3.2:1b
ollama pull nomic-embed-text
cd ch10/spring_ai/rag_retrieval
mvn spring-boot:run
```

## Output

The app prints an answer grounded in the local notes.
