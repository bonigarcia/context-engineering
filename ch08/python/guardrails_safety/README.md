# Output validation with Guardrails AI

This example demonstrates how to use the [Guardrails AI](https://github.com/guardrails-ai/guardrails) framework to enforce structural and safety constraints on the outputs of large language models. The provided script uses a Pydantic schema to define the expected format and includes a specialized validator to filter out inappropriate content. This approach ensures that the model outputs are safe and reliable for downstream processing in production environments.

## Requirements

* Python 3.9+.
* Libraries listed in `requirements.txt`.
* A Guardrails Hub token (available at https://hub.guardrailsai.com/keys).
* Profanity-free validator from [Guardrails Hub](https://guardrailsai.com/hub).

## Steps for running this example

1. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure Guardrails with your API token:
```bash
guardrails configure
```

3. Install the profanity-free validator:
```bash
guardrails hub install hub://guardrails/profanity_free
```

4. Run the Guardrails script:
```bash
python guardrails_example.py
```

## Output

The script will validate a JSON string against a Pydantic schema and run safety checks.

```text
Validating LLM output...
Validation successful!
Validated Output: {'summary': 'The system is working perfectly and the context is clear.', 'confidence': 0.95}

Simulating failed validation (content check)...
Cleaned Output: {'summary': 'The system is absolute [BAD_WORD] and failing.', 'confidence': 0.1}
```