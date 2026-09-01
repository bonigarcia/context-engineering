# Chat memory with LangChain4j and Ollama

This example shows how a bounded message window carries conversational state across turns.

The first call states a fact, and the second one relies on the memory window to recall it.

## Requirements

* [Java](https://www.oracle.com/java/technologies/downloads/) 21+
* [Maven](https://maven.apache.org/) 3.9+
* [Ollama](https://ollama.com/) installed locally
* A pulled chat model such as `llama3.2:1b`

## Steps for running this example in the shell

1. Start Ollama and pull the model:
```bash
ollama serve
ollama pull llama3.2:1b
```

2. Run the application:
```bash
mvn compile exec:java
```

## Output

```
Nice to meet you, Boni.
Your name is Boni.
```
