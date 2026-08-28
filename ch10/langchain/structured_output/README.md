# Structured output with LangChain core primitives

This example demonstrates the [LangChain](https://docs.langchain.com/) core primitives: initializing a chat model through the provider-agnostic factory and binding an output schema so that the response arrives as a validated object instead of free text.

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
python structured_output.py
```

## Output

When you run the script, it will send a user prompt to the LLM as input (*Capital of France?*) and the model should return an object validated against the `CityAnswer` schema (*city='Paris' country='France'*).
