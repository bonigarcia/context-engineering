# Function calling: current time

This example demonstrates the *function-calling loop* pattern using an [OpenAI](https://openai.com/) GPT model in JavaScript. In this pattern, the model can call external functions to get information. The loop is in the smallest useful form: the model decides when it needs external data, calls a function, and then uses the function result to answer.

## Requirements

* [Node.js](https://nodejs.org/) 18+
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
npm install
```

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
npm start
```

## Output

When you run the script, it will send a fixed user prompt (`What time is it right now?`) to a GPT model (`gpt-4o-mini`). The model will determine that it needs to call the `get_current_time` function to answer the question, and it will do so with the specified format. The application will execute the function, get the current time, and inject it back into the conversation as a `tool` message. Finally, the model will produce a user-facing answer grounded in the tool result.

```
User: What time is it right now?
        Tool requested: get_current_time({"format":"%Y-%m-%d %H:%M:%S"})
Assistant: The current time is 2026-03-25 19:17:32.
```
