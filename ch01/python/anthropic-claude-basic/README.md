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

When you run the script, it will send a user prompt to a Claude model (`claude-3-haiku-20240307`) using the parameters of `temperature` and `max_output_tokens`. Then, it will send the same user prompt to a more advanced model (`claude-sonnet-4-20250514`) using reasoning. The output will show the responses from both models.

```
=== Basic model  ===
User: How many tokens is your context window?
Claude3: I do not actually have a fixed context window size. I am an AI assistant created by Anthropic to be helpful, harmless, and honest. I don't have the same architectural details as language models that use a sliding context window. My responses are generated based on my training by Anthropic, not a fixed-size context.
=== Advanced model  ===
User: How many tokens is your context window?
Claude4: My context window is approximately 200,000 tokens. This means I can process and maintain context over roughly 200,000 tokens of text in a single conversation, which typically translates to around 150,000-200,000 words depending on the language and content type.
```