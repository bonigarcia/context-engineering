# Conversational state demo with Microsoft Agent Framework 

This example demonstrates *conversational state* in Microsoft Agent Framework using a custom `ContextProvider`. State is:

- Injected into the model before each turn.
- Updated after each turn.
- Persisted to disk (`conversation_state.json`).

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
python agent_conversational_state.py
```

## Output

This example illustrates how an AI agent can behave like a lightweight finite state machine rather than a stateless chatbot:

```
Stateful agent ready. Type 'exit' to quit.

Commands: /goal, /plan, /next, /state, /reset

You: What should I work on today?

Agent: What is your goal? You can say: /goal <text>.

You: /goal Learn Microsoft Agent Framework

Agent: Great goal! How would you like to start learning the Microsoft Agent Framework? Do you need resources, a study plan, or something else?

You: /state

(state file snapshot)
{
  "goal": "Learn Microsoft Agent Framework",
  "plan": [],
  "current_step_index": 0,
  "completed_steps": []
}

You: What should I do first?

Agent: I can propose a plan to start learning the Microsoft Agent Framework. Here's a short plan:

1. Research and gather introductory materials on the Microsoft Agent Framework.
2. Set up your development environment (install any necessary software).
3. Follow a tutorial or example project to create a simple agent.
4. Experiment with customizing the agent's behavior and appearance.
5. Review documentation for more advanced features.

Would you like to confirm this plan?

You: /plan

Agent: I've set the following plan for learning the Microsoft Agent Framework:

1. Research and gather introductory materials on the Microsoft Agent Framework.
2. Set up your development environment (install any necessary software).
3. Follow a tutorial or example project to create a simple agent.
4. Experiment with customizing the agent's behavior and appearance.
5. Review documentation for more advanced features.

Let's start with Step 1. Do you need help finding resources or materials?
```