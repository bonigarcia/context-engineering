# Streaming with Spring AI and Ollama

This example shows streaming model output — tokens arrive one by one
instead of all at once. Reads the prompt from standard input.

Uses `ChatClient.prompt().stream().content().subscribe()` to print
tokens as they arrive, with a `CountDownLatch` keeping the process alive
until the stream completes.

## Requirements

* Java 21+, Maven 3.9+, Ollama with `llama3.2:1b`

## Steps

```
ollama serve
ollama pull llama3.2:1b
mvn spring-boot:run
```

## Example session

```
Enter your prompt: Who are you?
Model: I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."
```