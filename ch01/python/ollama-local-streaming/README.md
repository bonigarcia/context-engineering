# Streaming responses from a local LLM using Ollama

This example demonstrates how to stream the response of a local LLM through the [Ollama](https://ollama.com/) HTTP API using Python. Instead of waiting for the complete answer, the script prints each fragment as the model produces it and reports the time to first token.

## Requirements

* [Python](https://www.python.org/) 3.8+
* [Ollama](https://ollama.com/) installed and running locally
* A local model pulled with Ollama, such as `gemma3:4b`

## Steps for running this example in the shell

1. Install the model in Ollama:
```bash
ollama pull gemma3:4b
```

2. Install dependencies:
```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

3. Run the script:
```bash
python ollama-local-streaming.py
```

## Optional environment variables

* `OLLAMA_HOST` defaults to `http://localhost:11434`
* `OLLAMA_MODEL` defaults to `gemma3:4b`

## Output

When you run the script, it sends a prompt to a local model through Ollama and prints the answer as it is generated. Once the stream ends, it prints the model name, the time to first token, the total latency, and the token counts reported by the local API. The timings depend on your hardware and on the model you have pulled.
