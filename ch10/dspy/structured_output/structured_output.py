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


class ActionPlan(dspy.Signature):
    """Turn a request into a compact action plan."""

    request: str = dspy.InputField(desc="short project request")
    summary: str = dspy.OutputField(desc="one-sentence summary")
    owner: str = dspy.OutputField(desc="best owner or team")
    priority: str = dspy.OutputField(desc="priority label: low, medium, or high")
    next_step: str = dspy.OutputField(desc="next action")


class LocalPlanningLM(dspy.BaseLM):
    def forward(self, prompt=None, messages=None, **kwargs):
        request_text = _extract_text(prompt, messages)
        payload = _plan_request(request_text)
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


def _plan_request(text: str) -> dict[str, str]:
    if any(keyword in text for keyword in ["refund", "charged twice", "billing", "invoice"]):
        return {
            "summary": "Handle the billing request and confirm the refund workflow.",
            "owner": "billing",
            "priority": "high",
            "next_step": "Verify the charge, then send the refund confirmation.",
        }

    if any(keyword in text for keyword in ["password", "login", "sign in", "access"]):
        return {
            "summary": "Restore account access and clear the login blocker.",
            "owner": "support",
            "priority": "high",
            "next_step": "Guide the user through the reset flow and confirm access.",
        }

    if any(keyword in text for keyword in ["launch", "release", "announcement"]):
        return {
            "summary": "Prepare a launch response for the request.",
            "owner": "product",
            "priority": "medium",
            "next_step": "Draft the message, review the rollout notes, and share it with the team.",
        }

    return {
        "summary": "Route the request to the right team and keep the reply short.",
        "owner": "support",
        "priority": "low",
        "next_step": "Acknowledge the request and forward it to the appropriate owner.",
    }


def run_demo() -> None:
    dspy.settings.configure(lm=LocalPlanningLM("local/structured-output"), adapter=dspy.JSONAdapter())
    planner = dspy.Predict(ActionPlan)

    requests = [
        "We were charged twice for the enterprise plan and need a refund.",
        "The customer cannot sign in after resetting the password.",
        "Please prepare a launch response for the product announcement.",
    ]

    for index, request in enumerate(requests, start=1):
        prediction = planner(request=request)
        print(f"Request {index}: {request}")
        print(f"Summary: {prediction.summary}")
        print(f"Owner: {prediction.owner}")
        print(f"Priority: {prediction.priority}")
        print(f"Next step: {prediction.next_step}")
        print()


if __name__ == "__main__":
    run_demo()
