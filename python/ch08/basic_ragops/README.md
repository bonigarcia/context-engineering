# Basic RAGOps example

This example implements a minimal Retrieval Augmented Generation (ATG) pipeline with operational logging, deterministic indexing, enforced citation formatting, and automated regression checks to illustrate core RAGOps practices.

## Requirements

This project requires [Python](https://www.python.org/) 3.x, the libraries listed in `requirements.txt`, and an OpenAI API key `OPENAI_API_KEY` as environment variable.

## Steps for running this example

1. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the script:
```bash
python basic_ragops.py
```

## Output

The program prints:

1. The input query
2. The generated answer
3. The result of a regression style validation step