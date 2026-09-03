# Combined context with Spring AI and Ollama

This example demonstrates four context sources working together:
system instructions, tools, RAG (external knowledge), and chat memory.

## Requirements

* Java 21+
* Maven 3.9+
* Ollama installed locally
* Pulled models: `llama3.2:3b`, `nomic-embed-text`

## Steps

1. Start Ollama and pull the models:
```bash
ollama serve
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

2. Run the application:
```bash
mvn spring-boot:run
```

## Output

The model answers using retrieved documents, calls a math tool, and recalls the conversation history.

```
User: How do I reset my password?
Model: To reset your password, please use the self-service portal. Once you have changed your password, sign in again to confirm the change.
User: What is 12 + 30?
Model: The answer is 42.
User: What was my first question?
Model: Your first question was "How do I reset my password?"
```