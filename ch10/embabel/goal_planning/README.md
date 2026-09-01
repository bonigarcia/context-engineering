# Goal planning with Embabel and Ollama

This example shows the planner choosing between two routes to the same goal.

Both `lookUpAnswer` and `generateAnswer` produce an `Answer`, and the first one is declared cheaper. The planner tries the cheap route first, and when the lookup returns nothing it replans and takes the model route. The action costs, not a hand-written branch, decide the order.

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
Open the local client and choose the office profile. (from knowledge base)
Update the billing address on the account settings page before the next invoice is issued. (from model)
```
