# Reranking

This example shows how a Haystack pipeline can retrieve locally and then rerank the results with a lightweight, deterministic scorer.

## Requirements

* [Python](https://www.python.org/) 3.10+

## Steps for running this example in the shell

1. Install dependencies:
```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Run the script:
```bash
python haystack_reranking.py
```

## Output

```
Question: Where do I find important notes?
Reranked results:
- Important notes: Important notes stay pinned at the top of the workspace.
- Tagging notes: Tagging groups related notes by project or topic.
- Archiving notes: Archived notes remain searchable after the task is done.
```
