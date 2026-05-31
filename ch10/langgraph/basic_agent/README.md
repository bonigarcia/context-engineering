# Basic LangGraph agent for stateful workflows

This example demonstrates a fundamental application of LangGraph, an extension of LangChain designed for building stateful, multi-actor applications with LLMs. It illustrates how to define a simple computational graph with a single LLM node and explicit state, allowing the workflow to keep the model output visible without redundant end-node processing.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [OpenAI API key](https://platform.openai.com/api-keys) set as an environment variable (`OPENAI_API_KEY`)

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

2. Export your API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python langgraph_basic_agent.py
```

## Output

When you run the script, it will execute a simple LangGraph workflow twice with different initial inputs. You will see a print statement indicating the LLM node (`---CALL_LLM---`), followed by the final state, which includes the LLM's response. This demonstrates how the `output` field in the `GraphState` is updated and carried through the graph.

Example output:

```
---CALL_LLM---
Initial Input: Hello, how are you today?
Final Output: I am an AI, so I don't have feelings, but I'm ready to assist you! How can I help you today?

---CALL_LLM---
Initial Input 2: What is the capital of France?
Final Output 2: The capital of France is Paris.
```
