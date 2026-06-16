# Context as code: Jinja2 prompt template with a CI evaluation gate

This example treats a prompt template as a versioned artifact and uses a small Python evaluator. The prompt lives in `prompt_template.j2`, the regression cases live in `test_cases.json`, and `evaluate_prompt.py` renders the Jinja2 template before calling an LLM. A GitHub Actions workflow in `.github/workflows/ch09_context_as_code.yml` runs the same evaluator on push and pull requests.

## Requirements

* Python 3.12+.
* The libraries listed in `requirements.txt`.
* An OpenAI API key exported as `OPENAI_API_KEY`.

## Steps for running this example

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

2. Run the evaluator:
```bash
python evaluate_prompt.py
```

3. To use the same check in GitHub Actions, configure `OPENAI_API_KEY` as a repository secret and let `.github/workflows/ch09_context_as_code.yml` run on pull requests.

## Output

When the prompt behaves as expected, the script prints one line per case and exits with status code `0`.

```text
[INFO] Evaluating prompt template with gpt-4o-mini...
[PASS] checkout outage: expected=urgent, actual=urgent
[PASS] password reset: expected=normal, actual=normal
[PASS] double charge: expected=urgent, actual=urgent
[INFO] Passed 3/3 checks.
```

If a prompt change regresses classification behavior, the script exits with status code `1`, which makes it suitable for a CI gate.
