# Basic RAG example with LlamaIndex

This example demonstrates a basic Retrieval-Augmented Generation (RAG) setup using LlamaIndex. It loads text from a local file, creates a vector store index, and then queries the index to retrieve relevant information.

## Requirements

* [Python](https://www.python.org/) 3.8+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

3. Run the script:
```bash
python rag_basic.py
```

## Output

The script will print the answer to the query "What is LlamaIndex?" based on the content of the `data.txt` file.
