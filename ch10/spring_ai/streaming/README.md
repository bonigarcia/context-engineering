# Streaming with Spring AI and Ollama

This example shows streaming model output — tokens arrive one by one
instead of all at once.

Uses `ChatClient.prompt().stream().content()` which returns a
`Flux<String>` of response chunks printed as they arrive.

## Requirements

* Java 21+, Maven 3.9+, Ollama with `llama3.2:1b`

## Steps

```
ollama serve
ollama pull llama3.2:1b
mvn spring-boot:run
```

## Output

Tokens appear incrementally on the same line:

```
User: Tell me a short joke about programming.
Model: Why do programmers prefer dark mode? Because light attracts bugs!
```