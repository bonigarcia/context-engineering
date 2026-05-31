# Reranking

This example shows how a Haystack pipeline can retrieve locally and then rerank the results with a lightweight, deterministic scorer.

## Requirements

- Python 3.10+
- `haystack-ai`

## Run

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python haystack_reranking.py
```

The reranker boosts exact title matches and query overlap so the most relevant note surfaces first.
