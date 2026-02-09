# Multi-agent router pattern

This example demonstrates the **router multi-agent pattern** using `langgraph`. It simulates a customer support system that intelligently routes user questions to specialized agents (sales, technical support, or general) based on the query's intent.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the following libraries:

* langchain
* langgraph
* langchain-openai
* python-dotenv

All dependencies are listed in `requirements.txt` and can be installed from there.

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
python multi_agent_router.py
```

## Output

The script will run three example questions, demonstrating how the system routes each query to the appropriate specialized agent and generates a response.
