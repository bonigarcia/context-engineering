# Simple stateful agent loop

This example demonstrates a minimal, stateful, single-agent loop. An agent, acting as a researcher, iteratively deepens its understanding of a topic over a fixed number of cycles.

The core concept illustrated is the explicit management of a **state object**. The agent's behavior at each step is determined by the current state, and its actions, in turn, update that state:

1. State initialization: A Python dictionary `agent_state` is created to hold the `topic`, `research_summary`, and `iteration_count`.
2. Agent loop: The script loops for a predefined number of iterations.
3. State-driven prompts: In each iteration, the prompt sent to the LLM is constructed based on the current `research_summary` and `iteration_count`.
4. State update: The LLM's response is used to update the `research_summary` in the state object, preparing it for the next iteration.

This example uses a simple `while` loop and a dictionary to manage state, showing how agentic behavior can be orchestrated without complex frameworks.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the following libraries:

* langchain-openai
* python-dotenv

All dependencies are listed in `requirements.txt` and can be installed from there.

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
```
python stateful_loop.py
```

## Output

The script will print the state at each step of the loop, showing how the research summary is progressively built.