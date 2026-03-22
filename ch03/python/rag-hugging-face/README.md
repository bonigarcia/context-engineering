# RAG with Hugging Face

This example demonstrates a complete RAG (Retrieval-Augmented Generation) pipeline using [Hugging Face](https://huggingface.co/) models and local retrieval.

The pipeline follows these steps:
1. Build a knowledge base: A small set of documents.
2. Chunk the documents: Splitting text into smaller passages.
3. Retrieve top-k chunks: Using TF-IDF and cosine similarity (scikit-learn).
4. Construct a prompt: Injecting retrieved context into a template.
5. Generate an answer: Using a Hugging Face model (`google/flan-t5-base`).
6. Show citations: Linking the answer back to the sources.

## Requirements

* [Python](https://www.python.org/) 3.8+
* Dependencies listed in `requirements.txt`

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the script:
```bash
python rag-hugging-face.py
```

## Output

The script will retrieve relevant chunks for the question "Why is chunking useful in RAG?" and generate a grounded answer using the local LLM.

```
User Query: Why is chunking useful in RAG?

ANSWER:

preserve context near boundaries.

CITATIONS:
  - 1. Chunking [doc2#chunk0]  (score=0.166)
  - 2. What is RAG? [doc1#chunk0]  (score=0.141)
  - 3. Similarity [doc3#chunk0]  (score=0.000)
```
