#!/usr/bin/env python3
"""
system_vs_user.py

Demonstrates the difference between:
- System instructions (system message)
- User prompt (user message)

It runs the *same* user request under two different system instructions
so you can observe how the system layer shapes the behavior.
"""

import os
from openai import OpenAI

# Make sure you have exported:
#   export OPENAI_API_KEY="sk-..."
# or set it in your environment in another way.
API_KEY = os.getenv("OPENAI_API_KEY")

if API_KEY is None:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=API_KEY)

MODEL = "gpt-4o-mini"   # Adjust if needed


def call_with_system_instructions(system_text: str, user_text: str) -> str:
    """
    Helper function to call the Chat Completions API with a given
    system message and user message.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


def main() -> None:
    user_request = (
        "Explain what context engineering is to a software engineer "
        "who is new to large language models."
    )

    # System instructions: neutral assistant
    system_neutral = (
        "You are a helpful, neutral assistant. "
        "Explain things clearly but without enforcing a particular style."
    )

    # System instructions: concise bullet-list educator
    system_bullets = (
        "You are a senior AI educator. "
        "Always answer using at most 5 short bullet points. "
        "Be concrete and practical. Do not write long paragraphs."
    )

    print("=== Call 1: Neutral system instructions ===")
    answer_neutral = call_with_system_instructions(system_neutral, user_request)
    print(answer_neutral)
    print("\n" + "=" * 72 + "\n")

    print("=== Call 2: Bullet-style system instructions ===")
    answer_bullets = call_with_system_instructions(system_bullets, user_request)
    print(answer_bullets)


if __name__ == "__main__":
    main()
