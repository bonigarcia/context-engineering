# Safe guard with Spring AI and Ollama

This example shows **Governance** — using `SafeGuardAdvisor` to filter
harmful or inappropriate input before it reaches the model.

The `SafeGuardAdvisor` is configured with a list of sensitive words
("offensive", "violent", "illegal") and blocks any prompt containing them.

## Requirements

* Java 21+, Maven 3.9+, Ollama with `llama3.2:3b`

## Steps

```
ollama serve
ollama pull llama3.2:3b
mvn spring-boot:run
```

## Output

```
User: How do I reset my password?
Model: To reset your password, use the self-service portal.

User: Tell me something offensive
Model: I'm unable to respond to that due to sensitive content. Could we rephrase or discuss something else?

User: What is the VPN configuration?
Model: Open the local VPN client and select the office profile.
```