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
from __future__ import annotations

import argparse
import json
import os
from textwrap import dedent
from typing import Dict

from openai import OpenAI


DEFAULT_MODEL = os.getenv("MODEL", "gpt-4o-mini")


def extract_issue(client: OpenAI, model: str, message: str) -> Dict[str, str]:
    """First chain step: turn an unstructured message into a structured record."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract the key support fields from a customer message. "
                    "Return only valid JSON with the keys product, issue, sentiment, urgency, and next_action."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Customer message:\n"
                    "The dashboard keeps logging me out when I switch tabs. I need to sign in again every time."
                ),
            },
            {
                "role": "assistant",
                "content": json.dumps(
                    {
                        "product": "dashboard",
                        "issue": "Session expires or resets when switching tabs",
                        "sentiment": "frustrated",
                        "urgency": "medium",
                        "next_action": "Check session persistence and browser lifecycle handling.",
                    },
                    indent=2,
                ),
            },
            {
                "role": "user",
                "content": f"Customer message:\n{message}\n\nReturn only JSON.",
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)


def draft_reply(client: OpenAI, model: str, extracted: Dict[str, str]) -> str:
    """Second chain step: use the structured context to draft the customer reply."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a support agent. Write a concise reply that acknowledges the issue, "
                    "summarizes the next step, and stays professional and empathetic."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Use this structured context to draft the reply:\n"
                    f"{json.dumps(extracted, indent=2)}\n\n"
                    "Write 3 to 4 sentences. Do not mention the JSON fields."
                ),
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Prompt chaining support reply")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set")

    client = OpenAI()
    message = dedent(
        """
        I keep getting signed out of the app whenever I move between dashboard tabs.
        It is happening on both Chrome and Edge, and it is slowing down our team.
        """
    ).strip()

    extracted = extract_issue(client, args.model, message)
    reply = draft_reply(client, args.model, extracted)

    print("=== Prompt chaining support reply ===")
    print("Customer message:")
    print(message)
    print("\nStep 1: extracted context")
    print(json.dumps(extracted, indent=2))
    print("\nStep 2: support reply")
    print(reply)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
