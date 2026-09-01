# Retrieval with LangChain4j and Ollama

This example shows a small local retrieval flow using Ollama embeddings and an in-memory embedding store.

Three short notes are ingested, the best match is retrieved for the question, and the retrieved note is the only external knowledge the model receives.

## Requirements

* [Java](https://www.oracle.com/java/technologies/downloads/) 21+
* [Maven](https://maven.apache.org/) 3.9+
* [Ollama](https://ollama.com/) installed locally
* A pulled chat model such as `llama3.2:1b`
* A pulled embedding model such as `nomic-embed-text`

## Steps for running this example in the shell

1. Start Ollama and pull the models:
```bash
ollama serve
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

2. Run the application:
```bash
mvn compile exec:java
```

## Output

```
Use the self-service portal to reset your password, then sign in again.
```
