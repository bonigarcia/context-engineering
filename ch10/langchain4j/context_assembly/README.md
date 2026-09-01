# Context assembly with LangChain4j and Ollama

This example is the one shown in the book. It wires four context sources into a single AI service: the system instruction, a bounded chat memory, a content retriever, and a tool object.

Three questions exercise the three sources in turn, so the console output shows which one answered each turn.

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
42
You first asked how to reset your password.
```
