# Context-as-code: versioned and validated system instructions

This example demonstrates how to treat system instructions as code artifacts by storing them in a structured format (YAML), versioning them, and applying automated governance checks before using them in an LLM prompt.

## Requirements

This project requires [Python](https://www.python.org/) 3.x and the libraries listed in `requirements.txt`.

## Steps for running this example

1. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

2. Run the script:
```bash
python context_as_code.py
```

## Output

The script will load the system instructions, run a governance check, and display the final formatted system prompt.

```text
[INFO] Loading system instructions version 1.0.0...
[INFO] Running governance validation...
[SUCCESS] Governance check passed. No forbidden terms found.
[INFO] Final System Prompt:
You are a professional customer support assistant for a software company. Your goal is to provide clear and helpful answers to user questions while maintaining a polite tone.
Follow these rules:
- Always greet the user politely.
- Be concise and avoid technical jargon unless necessary.
- If you do not know the answer, state it clearly and offer to escalate to a human.
Constraints:
- Do not share internal server logs or sensitive infrastructure details.
- Do not make financial commitments on behalf of the company.
```
