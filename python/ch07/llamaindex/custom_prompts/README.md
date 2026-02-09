# Customizing prompts with LlamaIndex

This example demonstrates how to apply custom system instructions and query prompts within LlamaIndex to guide the behavior and output format of the Large Language Model (LLM). Custom prompts are a key aspect of context engineering, allowing developers to precisely control the interaction between the user's query, retrieved context, and the LLM's response generation.

## Requirements

* [Python](https://www.python.org/) 3.8+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

3. Run the script:
```bash
python custom_prompts.py
```

## Output

The script will demonstrate how the LLM responds to queries while adhering to the specified custom system and query prompts. You will see the system prompt, query prompt, query, and the LLM's concise answer.