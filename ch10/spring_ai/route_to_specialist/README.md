# Multi-agent routing with Spring AI and Ollama

This example demonstrates context orchestration by routing support questions
to specialist agents. A supervisor ChatClient uses a tool to dispatch each
query to the right specialist (password, VPN, or invoice), each with
isolated system instructions and RAG context.

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

Each question is routed to the appropriate specialist agent.

```
User: How do I reset my password?
Model: To reset your password, please go to our self-service portal at [portal URL] and click on 'Forgot Password'. Follow the prompts to reset your password. Once you've reset your password, log in to your account using the new password. If you encounter any issues or have trouble resetting your password, please contact our HR department for assistance with escalated requests.

User: How do I connect to the VPN?
Model: Note: I've rephrased the question to make it more general IT-related, as the original question was quite specific to VPN-related topics.

User: Can I get a copy of my last invoice?
Model: I didn't recognize the category "billing" for this question. Let me try again.

{"name": "routeToSpecialist", "parameters": {"category":"invoice","question":"Can I get a copy of my last invoice?"}}
```