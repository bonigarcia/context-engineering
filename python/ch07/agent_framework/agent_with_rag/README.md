# Agent with RAG using Microsoft Agent Framework

This example demonstrates how to augment an AI agent with Retrieval Augmented Generation (RAG) capabilities using  Microsoft Agent Framework . The agent will use provided external context to answer questions, ensuring responses are grounded in the given information.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Setup

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

3. Run the script:
```bash
python agent_with_rag.py
```

## Output

The script will demonstrate the agent's ability to answer questions based on the content of some external knowledge. You should observe responses that are specifically grounded in the provided context.

```
Agent ready. Ask a question (type 'exit' to quit).

You: What is the return policy?

Agent: The return policy allows customers to return items within 30 days of delivery. Items must be unused and in their original packaging. Refunds are issued within 5 business days after the inspection of the returned item (SourceId: policy-returns).

You: How quickly do I get my money back?

Agent: You can expect to receive your money back within **5 business days** after your returned item is inspected. To qualify for a refund, items must be returned within **30 days of delivery** and should be unused and in their original packaging.

For more specifics, you can refer to the Return Policy ([SourceId: policy-returns]).

You: Is shipping free for large purchases?

Agent: Yes, standard shipping is free for orders over $50. If your large purchase meets this threshold, you will qualify for free standard shipping. For more details, you can refer to the shipping policy [here](https://example.com/policy-shipping) (SourceId: policy-shipping).
```