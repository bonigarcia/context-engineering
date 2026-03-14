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

When you run the script, it will send a user prompt to a GPT model (`gpt-4o-mini`) using the parameters of `temperature` and `max_output_tokens`. Then, it will send the same user prompt to a more advanced model (`gpt-5`) using reasoning. The output will show the responses from both models. 

```
=== Basic model  ===
User: How many tokens is your context window?
GPT4: My context window can handle up to 8,192 tokens. This includes both the input and the output tokens. If you have any specific questions or need assistance, feel free to ask!
=== Advanced model  ===
User: How many tokens is your context window?
GPT5: About 128,000 tokens. Note that your prompt plus my reply must fit within that, so very long inputs reduce how much I can output before hitting the limit.
```