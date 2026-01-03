# Two agents sharing global state

This example demonstrates a minimal multi-agent pattern where two distinct agents collaborate on a task by reading from and writing to a shared global state.

The scenario involves a "writer-editor" duo working on a document. Their collaboration is coordinated entirely through a shared Python dictionary that represents the global state of the document:

1. Global state: A single Python dictionary, `document_state`, is defined globally. It holds the content of a document, editor feedback, and a `status` field (`writing`, `editing`, `finished`).
2. Writer agent: A function that checks if the `status` is `writing`. If it is, the agent generates a draft, updates the `draft_content` in the global state, and changes the `status` to `editing`.
3. Editor agent: A function that checks if the `status` is `editing`. If it is, the agent reads the `draft_content`, generates feedback, updates the `feedback` field, and changes the `status` to `finished`.
4. Orchestrator: A simple function sequentially calls both agents. The agents themselves decide whether to act based on the information they read from the shared global state. This demonstrates a very simple form of emergent, state-driven coordination.

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
python shared_state.py
```

## Output

The script will print the global state at each major step, showing how the `writer` and `editor` agents modify it in turn to complete the collaborative task.