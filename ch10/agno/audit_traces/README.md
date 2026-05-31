# Audit Traces

This companion would show how Agno traces record which context, tools, and outputs reached each run so operators can inspect behavior after the fact.

## Run

1. Install the dependencies from `requirements.txt`.
2. Set `OPENAI_API_KEY`.
3. Run `python audit_traces.py`.

The script stores trace data in `audit_traces.json` and prints the latest trace stats after the run.
