# Basic LangGraph agent for stateful workflows

This example demonstrates a fundamental application of LangGraph, an extension of LangChain designed for building stateful, multi-actor applications with LLMs. It illustrates how to define a simple computational graph with nodes representing LLM calls and state transitions, allowing for the management of internal state across different steps of a workflow.

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
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```
Alternatively, create a `.env` file in the source directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

3. Run the script:
```bash
python langgraph_basic_agent
```

## Output

When you run the script, it will execute a simple LangGraph workflow twice with different initial inputs. You will see print statements indicating the execution of each node (`---CALL_LLM---` and `---END_NODE---`), followed by the final state, which includes the LLM's response. This demonstrates how the `output` field in the `GraphState` is updated and carried through the graph.

Example output:

```
---CALL_LLM---
---END_NODE---

Initial Input: Hello, how are you today?
Final Output: I am an AI, so I don't have feelings, but I'm ready to assist you! How can I help you today?

---CALL_LLM---
---END_NODE---

Initial Input 2: What is the capital of France?
Final Output 2: The capital of France is Paris.
```
