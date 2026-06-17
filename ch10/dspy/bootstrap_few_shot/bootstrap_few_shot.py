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


class ActionPlan(dspy.Signature):
    """Turn a request into a compact action plan."""

    request: str = dspy.InputField(desc="short project request")
    summary: str = dspy.OutputField(desc="one-sentence summary")
    owner: str = dspy.OutputField(desc="best owner or team")


trainset = [
    dspy.Example(
        request="Review the annual plan",
        summary="Review the annual plan before publication",
        owner="Strategy team",
    ).with_inputs("request"),
]


def owner_matches(example, prediction, trace=None):
    return prediction.owner.lower() == example.owner.lower()


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
    if any(keyword in text for keyword in ["annual plan", "strategy", "publication"]):
        return {
            "summary": "Review the annual plan before publication.",
            "owner": "Strategy team",
        }

    return {
        "summary": "Route the request to the right team.",
        "owner": "Support team",
    }


def main() -> None:
    dspy.settings.configure(lm=LocalPlanningLM("local/bootstrap-few-shot"), adapter=dspy.JSONAdapter())
    planner = dspy.Predict(ActionPlan)
    optimizer = dspy.BootstrapFewShot(metric=owner_matches)
    optimized_planner = optimizer.compile(planner, trainset=trainset)

    prediction = optimized_planner(request="Review the annual plan")
    print(f"Summary: {prediction.summary}")
    print(f"Owner: {prediction.owner}")


if __name__ == "__main__":
    main()
