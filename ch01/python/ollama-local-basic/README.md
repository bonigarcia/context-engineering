# Basic interaction with a local LLM using Ollama

This example demonstrates how to call a local LLM through the [Ollama](https://ollama.com/) HTTP API using Python.

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
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the script:
```bash
python ollama-local-basic.py
```

## Optional environment variables

* `OLLAMA_HOST` defaults to `http://localhost:11434`
* `OLLAMA_MODEL` defaults to `gemma3:4b`

## Output

When you run the script, it sends a prompt to a local model through Ollama and prints latency and token counts returned by the local API.

```
User: How many tokens is your context window?
        Model: gemma3:4b
        Latency: 12.546 seconds
        Input tokens: 17
        Output tokens: 147
        Total tokens: 164
Local LLM: As of today, November 2, 2023, my context window is **128,000 tokens**.

That's a *huge* amount of text! It allows me to understand and respond to very complex and detailed prompts, and to maintain context over long conversations.

**Important Note:** This refers to the *total* number of tokens in the prompt and my response combined.  So, a very long prompt will reduce the amount of space available for my response.

You can learn more about tokens and how they work here: [https://blog.openai.com/understanding-openai-tokens/](https://blog.openai.com/understanding-openai-tokens/)
```
