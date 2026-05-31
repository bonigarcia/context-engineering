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
from types import SimpleNamespace

import dspy


class TicketTriage(dspy.Signature):
    """Classify a support ticket and draft a short reply."""

    ticket: str = dspy.InputField(desc="support ticket text")
    priority: str = dspy.OutputField(desc="priority label: low, medium, or high")
    team: str = dspy.OutputField(desc="best team to handle the ticket")
    reply: str = dspy.OutputField(desc="short customer-facing reply")


class LocalTicketLM(dspy.BaseLM):
    def forward(self, prompt=None, messages=None, **kwargs):
        ticket_text = _extract_ticket_text(prompt, messages)
        triage = _triage_ticket(ticket_text)
        content = json.dumps(triage, ensure_ascii=False)

        return SimpleNamespace(
            model=self.model,
            choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
            usage={},
        )


def _extract_ticket_text(prompt, messages) -> str:
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


def _triage_ticket(text: str) -> dict[str, str]:
    if any(keyword in text for keyword in ["refund", "charged twice", "billing", "invoice"]):
        return {
            "priority": "high",
            "team": "billing",
            "reply": "Thanks for the details. I am routing this to billing now and will help get it resolved.",
        }

    if any(keyword in text for keyword in ["password", "login", "sign in", "access"]):
        return {
            "priority": "high",
            "team": "support",
            "reply": "Thanks. I am routing this to support so we can help restore your access quickly.",
        }

    if any(keyword in text for keyword in ["error", "bug", "crash", "broken"]):
        return {
            "priority": "medium",
            "team": "engineering",
            "reply": "Thanks for reporting this. I am sending it to engineering for a closer look.",
        }

    return {
        "priority": "low",
        "team": "support",
        "reply": "Thanks for reaching out. I am forwarding this to the right team and will follow up soon.",
    }


def run_demo() -> None:
    dspy.settings.configure(lm=LocalTicketLM("local/ticket-triage"), adapter=dspy.JSONAdapter())
    triage = dspy.Predict(TicketTriage)

    tickets = [
        "I was charged twice for my subscription and need a refund.",
        "I cannot log in after resetting my password.",
        "The dashboard export button is broken and shows an error.",
    ]

    for index, ticket in enumerate(tickets, start=1):
        prediction = triage(ticket=ticket)
        print(f"Ticket {index}: {ticket}")
        print(f"Priority: {prediction.priority}")
        print(f"Team: {prediction.team}")
        print(f"Reply: {prediction.reply}")
        print()


if __name__ == "__main__":
    run_demo()
