# LangGraph review workflow

This example keeps the state visible as the graph drafts an answer with a model call, routes it through a conditional edge, and sends it to review when the request mentions a payment.

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
python review_workflow.py
```

## What it demonstrates

- Explicit `input`, `draft`, and `needs_review` state fields
- A drafting node that calls the model and writes its reply into the state
- A conditional edge that routes to human review or to the end of the graph
- Intermediate state preserved in the graph output

## Output

When you run the script, it will print the final state of two runs. The first request ends after the drafting node, and the second one mentions a payment, so it also passes through the review node and its draft is prefixed with *Reviewed:*.
