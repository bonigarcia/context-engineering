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


KNOWLEDGE_BASE = {
    "Reset password": "Use the self-service portal to reset your password and unlock the account.",
    "VPN access": "Open the local VPN client, choose the office profile, and reconnect.",
    "Invoice copy": "Open billing and download the latest invoice from the account page.",
}


class ContextAnswer(dspy.Signature):
    """Answer using the supplied local context."""

    question: str = dspy.InputField(desc="user question")
    context: str = dspy.InputField(desc="retrieved context snippets")
    answer: str = dspy.OutputField(desc="short answer grounded in the context")
    source: str = dspy.OutputField(desc="source snippet title")


class LocalContextLM(dspy.BaseLM):
    def forward(self, prompt=None, messages=None, **kwargs):
        request_text = _extract_text(prompt, messages)
        payload = _answer_from_context(request_text)
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


def _lookup_context(question: str, knowledge_base: dict[str, str]) -> str:
    question_text = question.lower()
    matches: list[str] = []

    rules = [
        ("Reset password", ["password", "login", "sign in"], "Reset password"),
        ("VPN access", ["vpn", "connect"], "VPN access"),
        ("Invoice copy", ["invoice", "billing"], "Invoice copy"),
    ]

    for title, keywords, lookup_key in rules:
        if any(keyword in question_text for keyword in keywords):
            text = knowledge_base[lookup_key]
            matches.append(f"{title}: {text}")

    if not matches:
        title, text = next(iter(knowledge_base.items()))
        matches.append(f"{title}: {text}")

    return "\n".join(matches)


def _answer_from_context(text: str) -> dict[str, str]:
    if any(keyword in text for keyword in ["password", "login", "sign in"]):
        return {
            "answer": "Use the self-service portal to reset the password, then retry the login.",
            "source": "Reset password",
        }

    if any(keyword in text for keyword in ["vpn", "connect"]):
        return {
            "answer": "Open the local VPN client, select the office profile, and reconnect.",
            "source": "VPN access",
        }

    if any(keyword in text for keyword in ["invoice", "billing"]):
        return {
            "answer": "Download the latest invoice from the billing page.",
            "source": "Invoice copy",
        }

    return {
        "answer": "Check the local knowledge base and follow the documented steps.",
        "source": "Reset password",
    }


class ContextAwareAssistant(dspy.Module):
    def __init__(self, knowledge_base: dict[str, str] | None = None):
        super().__init__()
        self.knowledge_base = knowledge_base or KNOWLEDGE_BASE
        self.answer = dspy.Predict(ContextAnswer)

    def forward(self, question: str):
        context = _lookup_context(question, self.knowledge_base)
        return self.answer(question=question, context=context)


def run_demo() -> None:
    dspy.settings.configure(lm=LocalContextLM("local/context-tooling"), adapter=dspy.JSONAdapter())
    assistant = ContextAwareAssistant()

    questions = [
        "How do I reset my password?",
        "I cannot connect to the VPN from home.",
        "Where can I download the invoice copy?",
    ]

    for index, question in enumerate(questions, start=1):
        prediction = assistant(question=question)
        print(f"Question {index}: {question}")
        print(f"Answer: {prediction.answer}")
        print(f"Source: {prediction.source}")
        print()


if __name__ == "__main__":
    run_demo()
