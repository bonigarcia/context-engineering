# Function calling: current time

This example demonstrates the *function-calling* pattern using an [OpenAI](https://openai.com/) GPT model in Java. In this pattern, the model can call external functions to get information. The loop is in the smallest useful form: the model decides when it needs external data, calls a function, and then uses the function result to answer.

## Requirements

* [Java](https://www.oracle.com/java/technologies/downloads/) 21+
* [Maven](https://maven.apache.org/) 3.9+
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
mvn -q compile
```

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
mvn -q exec:java
```

## Output

When you run the script, it will send a fixed user prompt (`What time is it right now?`) to a GPT model (`gpt-4o-mini`). The model will determine that it needs to call the `GetCurrentTime` function to answer the question, and it will do so with the specified format. The application will execute the function and then send the result back to the model. Finally, the model will produce a user-facing answer grounded in the tool result.

```
User: What time is it right now?
	Tool requested: GetCurrentTime({"format":"yyyy-MM-dd HH:mm:ss"})
Assistant: The current time is 2026-03-25 18:50:27.
```
