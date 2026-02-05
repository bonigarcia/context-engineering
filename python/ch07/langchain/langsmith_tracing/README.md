# LangSmith tracing with LangChain

This example demonstrates how to enable and observe traces of your LangChain application using LangSmith. LangSmith is an essential platform for debugging, testing, evaluating, and monitoring Large Language Model (LLM) applications. By setting a few environment variables, you can automatically send detailed traces of your LangChain runs to your LangSmith project, providing deep visibility into context flow, intermediate steps, and LLM interactions.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. In addition, you must set the following environment variables to enable LangSmith tracing. You can find your `LANGCHAIN_API_KEY` on the LangSmith platform. Alternatively, create a `.env` file in the source directory with the content:

```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="YOUR_LANGSMITH_API_KEY"
LANGCHAIN_PROJECT="Your LangChain Project Name"
```

3. Run the script:
```bash
python langsmith_tracing.py
```

## Output

When you run the script, it will execute a simple LangChain sequence. The console output will show the question and answer. Crucially, in the background, a detailed trace of this execution will be sent to your LangSmith project. You will need to navigate to your LangSmith dashboard to view the trace, which will include:

*   The LLM call details.
*   The prompt used.
*   The LLM's response.
*   Metadata about the run.

Example console output:

```
--- Invoking LangChain with LangSmith tracing enabled ---
Question: What is the capital of Canada?
Answer: The capital of Canada is Ottawa.

--- To view the trace, visit your LangSmith project dashboard ---
Ensure LANGCHAIN_TRACING_V2=true and LANGCHAIN_API_KEY are set.
Look for a run in project: Context Engineering
```
