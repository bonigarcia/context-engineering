# Output validation with JSON Schema

This example demonstrates how to validate large language model outputs with a JSON Schema derived from a [Pydantic](https://pydantic.dev/) model. The provided script parses the model output, checks it against the schema, and then applies a simple policy rule that requires high-risk outputs to be escalated. This keeps the example installable and still shows how schema validation and business rules work together.

## Requirements

* Python 3.9+.
* Libraries listed in `requirements.txt`.

## Steps for running this example

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

2. Run the validation script:
```bash
python guardrails_example.py
```

## Output

The script validates a JSON string against a schema and then applies a simple escalation rule for high-risk outputs.

```text
Validating LLM output...
Validation successful!
Validated Output: {'summary': 'The request is low risk and can be answered directly.', 'risk_level': 'low', 'action': 'answer', 'citations': ['policy://general']}

Simulating policy failure (high risk must escalate)...
Policy validation failed as expected.
Validated Output: {'summary': 'The request requires review.', 'risk_level': 'high', 'action': 'answer', 'citations': ['policy://risk']}
```
