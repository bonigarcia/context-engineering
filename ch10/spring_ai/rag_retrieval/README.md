# Retrieval with Spring AI and Ollama

This example shows a tiny local RAG flow using Spring AI, Ollama embeddings, and an in-memory vector store.

It indexes a few short notes, retrieves the best match, and asks the chat model to answer from that context.

## Requirements

* [Java](https://www.oracle.com/java/technologies/downloads/) 21+
* [Maven](https://maven.apache.org/) 3.9+
* [Ollama](https://ollama.com/) installed locally
* A pulled chat model such as `llama3.2:1b`

## Steps for running this example in the shell

1. Start Ollama and pull the chat model:
```bash
ollama serve
ollama pull llama3.2:1b
```

2. Run the application:
```bash
mvn spring-boot:run
```

## Output

```
If you're having trouble finding this option or need help with the process, I'd be happy to try and assist you further. However, without more specific information about your situation, I'll need to inform you that I don't know what you're referring to by "invoice copy" or "VPN access". Could you provide more context or clarify what you're trying to reset?
```
