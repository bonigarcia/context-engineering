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

import json
import warnings
from types import SimpleNamespace

warnings.filterwarnings("ignore", category=DeprecationWarning)

import dspy


class ReasonedReply(dspy.Signature):
    """Write a brief reasoned reply."""

    question: str = dspy.InputField(desc="user question")
    reasoning: str = dspy.OutputField(desc="short reasoning string")
    answer: str = dspy.OutputField(desc="final answer")


class LocalReasoningLM(dspy.BaseLM):
    def forward(self, prompt=None, messages=None, **kwargs):
        request_text = _extract_text(prompt, messages)
        payload = _reason_about(request_text)
        content = json.dumps(payload, ensure_ascii=False)

        return SimpleNamespace(
            model=self.model,
            choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
            usage={},
        )


def _extract_text(prompt, messages) -> str:
    parts: list[str] = []
    if prompt:
        parts.append(str(prompt))
    for message in messages or []:
        content = message.get("content")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            parts.extend(str(item.get("text", item)) for item in content)
    return "\n".join(parts).lower()


def _reason_about(text: str) -> dict[str, str]:
    if any(keyword in text for keyword in ["deploy", "release", "launch"]):
        return {
            "reasoning": "A launch request needs a short plan and a clear final status.",
            "answer": "Summarize the release steps, confirm the rollout owner, and share the final checklist.",
        }

    if any(keyword in text for keyword in ["billing", "invoice", "refund"]):
        return {
            "reasoning": "Billing questions should confirm the charge and keep the reply precise.",
            "answer": "Verify the charge, explain the refund status, and point the user to billing support.",
        }

    return {
        "reasoning": "The safest answer is a short direct reply.",
        "answer": "Give the user a concise answer and the next concrete step.",
    }


def run_demo() -> None:
    dspy.settings.configure(lm=LocalReasoningLM("local/stepwise-reasoning"), adapter=dspy.JSONAdapter())
    responder = dspy.Predict(ReasonedReply)

    questions = [
        "How should we handle the product launch this week?",
        "What should we say about the duplicate billing report?",
    ]

    for index, question in enumerate(questions, start=1):
        prediction = responder(question=question)
        print(f"Question {index}: {question}")
        print(f"Reasoning: {prediction.reasoning}")
        print(f"Answer: {prediction.answer}")
        print()


if __name__ == "__main__":
    run_demo()
