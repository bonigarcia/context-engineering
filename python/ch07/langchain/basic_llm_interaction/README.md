# Basic interaction with an LLM using LangGraph

This example demonstrates how to set up a LLM (e.g., OpenAI), invoke a prompt, and parse its output using [LangChain](https://docs.langchain.com/).

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

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
Alternatively, create a `.env` file in the source directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

3. Run the script:
```bash
python basic_llm_interaction.py
```

## Output

When you run the script, it will send a basic user prompt to the LLM as input (*What is the capital of France?*) and the model should provide a response (*The capital of France is Paris*).