# Workflow state in Microsoft Agent Framework

This example is a minimal runnable example illustrating *state* in Microsoft Agent Framework workflows.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Setup

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
python workflow_state.py
```

## Output

This pattern is useful when large/structured data should be shared across steps without passing it through every message:

```
Temp file: /tmp/maf_state_demo_g8t8mqg0/sample.txt
Word count: 14
```