# Simple Stateful Agent Loop

This example demonstrates a minimal, stateful, single-agent loop. An agent, acting as a researcher, iteratively deepens its understanding of a topic over a fixed number of cycles.

The core concept illustrated is the explicit management of a **state object**. The agent's behavior at each step is determined by the current state, and its actions, in turn, update that state.

## How it Works

1.  **State Initialization**: A Python dictionary `agent_state` is created to hold the `topic`, `research_summary`, and `iteration_count`.
2.  **Agent Loop**: The script loops for a predefined number of iterations.
3.  **State-Driven Prompts**: In each iteration, the prompt sent to the LLM is constructed based on the current `research_summary` and `iteration_count`.
4.  **State Update**: The LLM's response is used to update the `research_summary` in the state object, preparing it for the next iteration.

This example uses a simple Python `while` loop and a dictionary to manage state, showing how agentic behavior can be orchestrated without complex frameworks.

## Setup

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set environment variables**:
    Create a `.env` file in this directory with your OpenAI API key:
    ```
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```

## Run the example

```bash
python stateful_loop.py
```
The script will print the state at each step of the loop, showing how the research summary is progressively built.
