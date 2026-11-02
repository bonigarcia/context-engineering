# Function calling

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

When you run the script, it will send a fixed user prompt (`What is the weather in San Francisco?`) to a GPT model (`gpt-6-luna`). The model will determine that it needs to call the `GetWeather` function to answer the question, and it will do so with the requested location. The application will execute the function and then send the result back to the model. Finally, the model will produce a user-facing answer grounded in the tool result.

```
User: What is the weather in San Francisco?
	Tool requested: GetWeather({"location":"San Francisco"})
Assistant: The current weather in San Francisco is sunny with a temperature of 18°C and a humidity level of 63%.
```
