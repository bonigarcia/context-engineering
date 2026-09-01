# Basic agent with Embabel and Ollama

This example shows the smallest Embabel agent: two actions and one goal.

No step order is written anywhere. The planner reads the parameter and return types of each action, finds that `classify` produces the `Ticket` that `draftReply` consumes, and builds the plan from those types.

## Requirements

* [Java](https://www.oracle.com/java/technologies/downloads/) 21+
* [Maven](https://maven.apache.org/) 3.9+
* [Ollama](https://ollama.com/) installed locally
* A pulled chat model such as `llama3.1:8b`

## Steps for running this example in the shell

1. Start Ollama and pull the chat model:
```bash
ollama serve
ollama pull llama3.1:8b
```

2. Run the application:
```bash
mvn spring-boot:run
```

## Output

```
Thanks for reaching out about the billing portal login issue. We have raised it with the access team and will confirm as soon as your sign-in is restored.
```
