"""
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import math
from typing import Dict
import dspy

# 1. Setup
# Make sure you have set the OPENAI_API_KEY environment variable
lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)


# 2. Signature definition
class MathQA(dspy.Signature):
    """
    Solve short math word problems and return the final numeric answer.

    The model receives a natural language question and should output only
    the final numeric answer as text (no units or extra commentary).
    """

    question: str = dspy.InputField(
        desc="a short math word problem stated in natural language"
    )
    answer: str = dspy.OutputField(
        desc="the final numeric answer only, without units or extra text"
    )


# 3. Chain-of-Thought module
def run_cot_example():
    cot_math_solver = dspy.ChainOfThought(MathQA)

    example_question = """
    A train travels 80 kilometers in 1 hour and 20 minutes.
    What is its average speed in kilometers per hour?
    """

    prediction = cot_math_solver(question=example_question)

    print("=== Chain-of-Thought prediction ===")
    print("Question:")
    print(example_question.strip())
    print("\nReasoning:")
    print(prediction.reasoning)
    print("\nAnswer:")
    print(prediction.answer)


# 4. ReAct agent with a calculator tool
def safe_calculator(expression: str) -> str:
    """
    Evaluate a basic arithmetic expression involving +, -, *, /, and parentheses.

    The tool returns the numeric result as a string.
    It is intended for simple math expressions extracted from short word problems.
    """

    allowed_names: Dict[str, object] = {
        "sqrt": math.sqrt,
        "ceil": math.ceil,
        "floor": math.floor,
    }

    try:
        # Note: eval() is used here for simplicity in a controlled example.
        # In production, use a dedicated math parser for security.
        result = eval(expression, {"__builtins__": {}}, allowed_names)
    except Exception as exc:
        return f"Error evaluating expression: {exc}"

    return str(result)


def run_react_example():
    react_math_agent = dspy.ReAct(
        signature=MathQA,
        tools=[safe_calculator],
        max_iters=5,
    )

    react_question = """
    A book costs 18 euros before tax. It is discounted by 15%,
    and then you buy 3 copies at the discounted price.
    What is the total amount you pay (ignoring tax), in euros?
    """

    prediction = react_math_agent(question=react_question)

    print("\n=== ReAct prediction ===")
    print("Question:")
    print(react_question.strip())
    print("\nAnswer:")
    print(prediction.answer)

    print("\n=== ReAct trajectory ===")
    print(prediction.trajectory)


if __name__ == "__main__":
    run_cot_example()
    run_react_example()
