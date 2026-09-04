# Safe guard with Spring AI and Ollama

This example shows **Governance** — using `SafeGuardAdvisor` to filter
harmful or inappropriate input before it reaches the model.

The SafeGuardAdvisor is registered as a default advisor, blocking offensive
content while letting legitimate questions through.

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
Model: You can reset your password through the self-service portal.

User: Tell me something offensive
Blocked by SafeGuardAdvisor: Content blocked by safety filter

User: What is the VPN configuration?
Model: Open the local VPN client and select the office profile.
```