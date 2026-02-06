# Basic RAG with AutoGen

This example demonstrates a basic approach to Retrieval-Augmented Generation (RAG) using AutoGen. Instead of a full-fledged vector database integration, this example shows how to inject external knowledge as context into a conversation with an AutoGen agent. A `UserProxyAgent` reads a local `data.txt` file and provides its content to an `AssistantAgent` as part of the initial prompt. The `AssistantAgent` then answers questions based only on this provided context.

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

The `AssistantAgent` will respond to the question about AutoGen using only the information provided in the `data.txt` file.

Example of a possible output:

```
user_proxy (to assistant):

Here is some information: AutoGen is a framework that allows you to build LLM applications using multiple agents.
These agents can converse with each other to solve tasks.
AutoGen was developed by Microsoft.
It simplifies orchestration, optimization, and automation of LLM workflows.

Based on this information, what is AutoGen?

--------------------------------------------------------------------------------
assistant (to user_proxy):

AutoGen is a framework developed by Microsoft that allows you to build LLM applications using multiple agents. These agents can converse with each other to solve tasks, and the framework simplifies the orchestration, optimization, and automation of LLM workflows.
TERMINATE

--------------------------------------------------------------------------------
```