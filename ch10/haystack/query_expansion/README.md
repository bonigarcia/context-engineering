# Query expansion

This example expands a user query into a few local variants, runs BM25 retrieval for each variant, and merges the results.

## Requirements

- Python 3.10+
- `haystack-ai`

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python haystack_query_expansion.py
```

The example keeps everything local while showing how recall improves when the query is broadened before retrieval.
