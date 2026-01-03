# Simple stateful agent loop

This example demonstrates a minimal, stateful, single-agent loop. An agent, acting as a researcher, iteratively deepens its understanding of a topic over a fixed number of cycles.

The core concept illustrated is the explicit management of a **state object**. The agent's behavior at each step is determined by the current state, and its actions, in turn, update that state:

1. State initialization: A Python dictionary `agent_state` is created to hold the `topic`, `research_summary`, and `iteration_count`.
2. Agent loop: The script loops for a predefined number of iterations.
3. State-driven prompts: In each iteration, the prompt sent to the LLM is constructed based on the current `research_summary` and `iteration_count`.
4. State update: The LLM's response is used to update the `research_summary` in the state object, preparing it for the next iteration.

This example uses a simple `while` loop and a dictionary to manage state, showing how agentic behavior can be orchestrated without complex frameworks.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2.  Set environment variables:
Create a `.env` file in this directory with your OpenAI API key:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

3. Run the script, that will print the state at each step of the loop, showing how the research summary is progressively built.
```
python stateful_loop.py
```

## Output

After running the script, you will see the agent's output over a fixed number of iterations.

```
--- Initial State ---
{'topic': 'The role of context engineering in AI', 'research_summary': '', 'iteration_count': 0, 'max_iterations': 3}

--- Iteration 1 ---
  Action: Generated initial summary.
  New Summary: "Context engineering in AI refers to the deliberate design and manipulation of contextual information..."

--- Iteration 2 ---
  Action: Identified next research step.
  New Summary: "Context engineering in AI refers to the deliberate design and manipulation of contextual information..."

--- Iteration 3 ---
  Action: Identified next research step.
  New Summary: "Context engineering in AI refers to the deliberate design and manipulation of contextual information..."

--- Final State ---
{'topic': 'The role of context engineering in AI', 'research_summary': "Context engineering in AI refers to the deliberate design and manipulation of contextual information to enhance the performance and relevance of artificial intelligence systems. This approach is crucial in enabling AI to understand and respond to human inputs more effectively by considering the situational, cultural, and environmental factors that influence meaning. By integrating context, AI systems can achieve more nuanced and accurate interpretations, leading to improved decision-making and user interactions. Context engineering is particularly significant in natural language processing, where understanding the subtleties of human language requires awareness of the surrounding context. As AI continues to evolve, the role of context engineering becomes increasingly important in developing systems that are not only technically proficient but also socially and culturally aware, thereby enhancing their applicability across diverse real-world scenarios.\n\nNext step: Investigate the methodologies and frameworks for effectively integrating cultural context into AI systems to enhance their cross-cultural understanding and interaction capabilities.\n\nNext step: Investigate the role of cultural ontologies and knowledge graphs in enhancing AI systems' ability to interpret and respond to diverse cultural contexts.", 'iteration_count': 3, 'max_iterations': 3}
```