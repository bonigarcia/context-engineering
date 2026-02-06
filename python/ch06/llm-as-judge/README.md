# Context evaluation with LLM-as-Judge using Ragas

This example demonstrates the **LLM-as-Judge** pattern for evaluating the quality of a Retrieval-Augmented Generation (RAG) system. It uses the `ragas` library, which leverages a large language model (LLM) to score the performance of a RAG pipeline across several key dimensions of context engineering.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

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
Alternatively, create a `.env` file in the source directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

3. Run the script:
```bash
python llm_as_judge.py
```

## Output

The script will first build a simple RAG pipeline and then run the `ragas` evaluation. The output will be the results from the evaluation, printed first as a Ragas object and then as a pandas DataFrame. The DataFrame includes scores for each metric (`faithfulness`, `answer_relevancy`, etc.) for every question in the evaluation dataset, providing a clear, quantitative assessment of the RAG system's performance.