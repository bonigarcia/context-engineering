# RAG pipeline

This example uses a local Haystack pipeline with an in-memory document store and BM25 retrieval.

## Requirements

- Python 3.10+
- `haystack-ai`

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python haystack_rag_pipeline.py
```

The script prints the top retrieved notes from the local corpus, so no API key or external service is required.
