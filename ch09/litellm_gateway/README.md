# LiteLLM gateway example

This example shows how an AI gateway can sit between an application and multiple model providers.

The script uses a [LiteLLM](https://www.litellm.ai/) client interface to send one request through a primary model and one through a fallback model. It uses mock responses so the example is easy to run without real provider credentials.


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

2. Run the script:
```bash
python litellm_gateway.py
```

## Output

```text
[INFO] Primary path selected: openai/gpt-6-luna
[INFO] Response: Primary provider answer.

Provider List: https://docs.litellm.ai/docs/providers

[INFO] Fallback path selected: anthropic/claude-haiku-4-5
[INFO] Response: Fallback provider answer.
```
