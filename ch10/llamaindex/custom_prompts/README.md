# Customizing prompts with LlamaIndex

This example demonstrates how to apply custom system instructions and query prompts within LlamaIndex to guide the behavior and output format of the Large Language Model (LLM). Custom prompts are a key aspect of context engineering, allowing developers to precisely control the interaction between the user's query, retrieved context, and the LLM's response generation.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [OpenAI API key](https://platform.openai.com/api-keys) set as an environment variable (`OPENAI_API_KEY`)

## Steps for running this example in the shell

1. Install dependencies:
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

2. Export your API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python custom_prompts.py
```

## Output

The script will demonstrate how the LLM responds to queries while adhering to the specified custom system and query prompts. You will see the system prompt, query prompt, query, and the LLM's concise answer.
