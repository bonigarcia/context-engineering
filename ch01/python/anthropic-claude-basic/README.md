# Basic interaction with Anthropic Claude models

This example demonstrates how to set up an [Anthropic Claude](https://www.anthropic.com/) model and send a basic user prompt with Python.

## Requirements

* [Python](https://www.python.org/) 3.6+
* An [Anthropic API key](https://platform.claude.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Export your Anthropic API key as an environment variable:
```bash
export ANTHROPIC_API_KEY="sk-..." # Windows cmd: set ANTHROPIC_API_KEY="sk-..." # Windows PowerShell: $env:ANTHROPIC_API_KEY="sk-..."
```

3. Run the script:
```bash
python anthropic-claude-basic.py
```

## Output

When you run the script, it will send a basic user prompt to the model, which should provide a response:

```
User: How many tokens is your context window?
AI: My context window is 200,000 tokens, which is quite large and allows me to work with substantial amounts of text in a single conversation. This means I can maintain context across long discussions, analyze lengthy documents, or work with complex multi-part problems while keeping track of all the relevant information throughout our conversation.
```