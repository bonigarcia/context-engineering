# Basic RAG with AutoGen

This example demonstrates a basic approach to Retrieval-Augmented Generation (RAG) using AutoGen. TODO.

## Requirements

* [Python](https://www.python.org/) 3.8+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

3. Create the `data.txt` file:
Ensure a file named `data.txt` exists in the same directory as `rag_with_autogen.py` with the following content:

```
AutoGen is a framework that allows you to build LLM applications using multiple agents.
These agents can converse with each other to solve tasks.
AutoGen was developed by Microsoft.
It simplifies orchestration, optimization, and automation of LLM workflows.
```

4. Run the script:
```bash
python rag_with_autogen.py
```

## Expected Output

TODO.