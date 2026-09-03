# Chat memory with Spring AI and Ollama

This example shows Spring AI remembering conversation context across turns
using `MessageChatMemoryAdvisor` and `MessageWindowChatMemory`.

## Requirements

* Java 21+
* Maven 3.9+
* Ollama installed locally
* A pulled chat model such as `llama3.2:3b`

## Steps

1. Start Ollama and pull the model:
```bash
ollama serve
ollama pull llama3.2:3b
```

2. Run the application:
```bash
mvn spring-boot:run
```

## Output

The model remembers the user's name from the first turn and recalls it in the second turn.
```
User: My name is John Snow.
Model: Nice to meet you, John Snow. Is there something I can help you with or would you like to chat about something in particular?
User: What is my name?
Model: I can answer that, John Snow. Your name is John Snow.
```