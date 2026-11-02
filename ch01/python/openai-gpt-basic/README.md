# Basic interaction with OpenAI GPT models

This example demonstrates how to set up an [OpenAI](https://openai.com/) GPT model and send a basic user prompt with Python.

## Requirements

* [Python](https://www.python.org/) 3.6+
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1.  Install dependencies:
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

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python openai-gpt-basic.py
```

## Output

When you run the script, it will send a user prompt to a GPT model (`gpt-6-luna`) with reasoning disabled, using the `temperature` parameter. Then, it will send the same user prompt to the same model with medium reasoning effort. The output will show both responses. 

```
=== Without reasoning ===
User: How many tokens are in your context window?
        Model: gpt-6-luna
        Latency: 5.145 seconds
        Input tokens: 15
        Output tokens: 19
        Reasoning tokens: 0
        Total tokens: 34
AI: I don’t have access to the exact context-window limit for this conversation.

=== With reasoning ===
User: How many tokens are in your context window?
        Model: gpt-6-luna
        Latency: 6.083 seconds
        Input tokens: 15
        Output tokens: 250
        Reasoning tokens: 210
        Total tokens: 265
AI: I can’t see the exact limit configured for this chat. Some versions support up to 128,000 tokens, but the actual limit can vary by model and setup.
```