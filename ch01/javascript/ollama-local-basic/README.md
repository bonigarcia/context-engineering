# Basic interaction with a local LLM using Ollama

This example demonstrates how to call a local LLM through the [Ollama](https://ollama.com/) HTTP API using JavaScript.

## Requirements

* [Node.js](https://nodejs.org/) 18+
* [Ollama](https://ollama.com/) installed and running locally
* A local model pulled with Ollama, such as `gemma3:4b`

## Steps for running this example in the shell

1. Install the model in Ollama:
```bash
ollama pull gemma3:4b
```

2. Install dependencies:
```bash
npm install
```

3. Run the script:
```bash
npm start
```

## Optional environment variables

* `OLLAMA_HOST` defaults to `http://localhost:11434`
* `OLLAMA_MODEL` defaults to `gemma3:4b`

## Output

When you run the script, it sends a prompt to a local model through Ollama and prints latency and token counts returned by the local API.

```
User: How many tokens is your context window?
        Model: gemma3:4b
        Latency: 10.746 seconds
        Input tokens: 17
        Output tokens: 147
        Total tokens: 164
Local LLM: As of today, November 2, 2023, my context window is **128,000 tokens**.

That's a *huge* amount of text! It allows me to understand and respond to very complex and detailed prompts, and to maintain context over long conversations.

**Important Note:** This refers to the *total* number of tokens in the prompt and my response combined.  So, a very long prompt will reduce the amount of space available for my response.

You can learn more about tokens and how they work here: [https://blog.openai.com/understanding-openai-tokens/](https://blog.openai.com/understanding-openai-tokens/)
```
