# Retrieval-Augmented Generation (RAG) with LangChain and FAISS

This example demonstrates how to implement a basic Retrieval-Augmented Generation (RAG) system using LangChain. It showcases loading a document, splitting it into chunks, generating embeddings, storing them in a FAISS vector store, and then retrieving relevant information to answer a query using an LLM.

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
python rag_with_vectorstore.py
```

## Output

When you run the script, it will perform the following actions:
1.  Create a temporary `sample_document.txt` with some dummy text.
2.  Load and split this document.
3.  Create embeddings and store them in an in-memory FAISS vector store.
4.  Retrieve relevant chunks for the question "What is RAG and why is it useful?".
5.  Use an LLM (GPT-4o) to answer the question based on the retrieved context.
6.  Print the query, the LLM's answer, and the metadata of the source documents used.
7.  Clean up the temporary `sample_document.txt`.

The output should look similar to this:

```
Query: What is RAG and why is it useful?
Response: RAG, or Retrieval-Augmented Generation, combines large language models with external knowledge bases. It is useful because it allows LLMs to retrieve relevant, up-to-date information, thereby generating more accurate and current responses.
Source Documents: [{}, {}]
```
(Note: The metadata for the source documents will be empty as they are generated on the fly for this example.)