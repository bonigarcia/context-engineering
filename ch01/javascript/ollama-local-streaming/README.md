# Streaming responses from a local LLM using Ollama

This example demonstrates how to stream the response of a local LLM through the [Ollama](https://ollama.com/) HTTP API using JavaScript. Instead of waiting for the complete answer, the script prints each fragment as the model produces it and reports the time to first token.

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

When you run the script, it sends a prompt to a local model through Ollama and prints the answer as it is generated. Once the stream ends, it prints the model name, the time to first token, the total latency, and the token counts reported by the local API. The timings depend on your hardware and on the model you have pulled.
