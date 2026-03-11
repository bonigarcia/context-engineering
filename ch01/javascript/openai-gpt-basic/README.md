# Basic interaction with OpenAI GPT models

This example demonstrates how to set up an [OpenAI](https://openai.com/) GPT model and send a basic user prompt with JavaScript.

## Requirements

* [Node.js](https://nodejs.org/)
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

When you run the script, it will send a basic user prompt to the model, which should provide a response:

```
User: How many tokens is your context window?
AI: My context window is 32,768 tokens. This means I can process and keep track of up to 32,768 tokens of text in a single conversation or input. If you have any other questions about how this works, feel free to ask!
```