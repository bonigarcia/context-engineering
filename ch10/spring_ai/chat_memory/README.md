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
Model: A legendary name, John Snow! I'm assuming you're not the same John Snow from the hit HBO series Game of Thrones, but rather a fan who shares a similar name.

If that's the case, I'd be happy to chat with you about the show or discuss other topics. Alternatively, if you're indeed the John Snow from Westeros, I'd be delighted to engage in a fantasy adventure with you!

Which direction would you like to take our conversation?
User: What is my name?
Model: I apologize for assuming earlier! Your name is indeed John Snow, and I should have just stuck with that. I'm here to help and chat with you about whatever you'd like. How's your day going, John Snow?
```