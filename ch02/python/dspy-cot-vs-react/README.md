# DSPy: Chain-of-Thought vs ReAct

This example demonstrates how to implement the same "math tutor" task with two different prompting strategies in [DSPy](https://dspy-docs.vercel.app/):

1.  A **Chain-of-Thought (CoT)** module that reasons step by step.
2.  A **ReAct** agent that can call a calculator tool while reasoning.

## Requirements

* [Python](https://www.python.org/) 3.6+
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python dspy_cot_vs_react.py
```

## Output

When you run the script, it will execute both the Chain-of-Thought and ReAct strategies and print their results and reasoning/trajectory.