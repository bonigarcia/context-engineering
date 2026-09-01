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
Model: To reset your password, please use the self-service portal to generate a new password. After generating a new password, sign in again with your new credentials.
User: What is 12 plus 30?
Model: 12 + 30 = 42
User: What was my first question?
Model: Your first question was about resetting your password.
```