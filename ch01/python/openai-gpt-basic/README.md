# Basic interaction with OpenAI GPT models

This example demonstrates how to set up an [OpenAI](https://openai.com/) GPT model and send a basic user prompt with Python.

## Requirements

* [Python](https://www.python.org/) 3.6+
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
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

When you run the script, it will send a user prompt to a GPT model (`gpt-4o-mini`) using the `temperature` parameter. Then, it will send the same user prompt to a more advanced model (`gpt-5`) using reasoning. The output will show the responses from both models. 

```
=== Basic model  ===
User: How many tokens is your context window?
        Model: gpt-4o-mini-2024-07-18
        Latency: 1.690 seconds
        Input tokens: 15
        Output tokens: 39
        Reasoning tokens: 0
        Total tokens: 54
GPT4: My context window can handle up to 8,192 tokens. This includes both the input and the output tokens. If you have any specific questions or need assistance, feel free to ask!

=== Advanced model  ===
User: How many tokens is your context window?
        Model: gpt-5-2025-08-07
        Latency: 10.785 seconds
        Input tokens: 14
        Output tokens: 544
        Reasoning tokens: 512
        Total tokens: 558
GPT5: About 128,000 tokens total (input + output combined).
```