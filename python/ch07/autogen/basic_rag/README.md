# Basic Retrieval-Augmented Generation (RAG) with AutoGen

This example demonstrates a basic RAG setup using AutoGen's `RetrieveUserProxyAgent`. It showcases how to configure agents to answer questions by retrieving information from specified external URLs.

## Requirements

* [Python](https://www.python.org/) 3.8+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

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
python basic_rag.py
```

## Expected Output

Upon running the script, the `RetrieveUserProxyAgent` will embed the specified documents and then engage in a conversation with the `AssistantAgent`. The output will show the chat history, where the agents collaborate to answer the `code_problem` by retrieving relevant information about using FLAML with Spark for parallel training. The final message from the assistant should contain the answer to the problem, followed by 'TERMINATE'.