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

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

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

```
=== Chain-of-Thought prediction ===
Question:
A train travels 80 kilometers in 1 hour and 20 minutes.
    What is its average speed in kilometers per hour?

Reasoning:
1 hour 20 minutes is \( \frac{4}{3} \) hours. Average speed is \(80 \div \frac{4}{3} = 60\).

Answer:
60

=== ReAct prediction ===
Question:
A book costs 18 euros before tax. It is discounted by 15%,
    and then you buy 3 copies at the discounted price.
    What is the total amount you pay (ignoring tax), in euros?

Answer:
45.9

=== ReAct trajectory ===
{'thought_0': 'The discounted price per book is 18 × 0.85, and for 3 copies the total is 18 × 0.85 × 3.', 'tool_name_0': 'safe_calculator', 'tool_args_0': {'expression': '18*0.85*3'}, 'observation_0': '45.9', 'thought_1': 'The total for 3 discounted books is 45.9 euros.', 'tool_name_1': 'finish', 'tool_args_1': {}, 'observation_1': 'Completed.'}
```