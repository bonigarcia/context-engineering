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


def analyze_inquiry(client: OpenAI, model: str, message: str) -> Dict[str, str]:
    """Step 1: Extract structured case classification and sentiment from the raw message."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Analyze the customer support inquiry. Return only valid JSON with the following keys: "
                    "category (one of: billing, technical_bug, feature_request, general_inquiry), "
                    "urgency (one of: low, medium, high, critical), "
                    "sentiment (one of: positive, neutral, frustrated, angry), "
                    "summary (a concise 1-sentence summary of the core issue)."
                ),
            },
            {
                "role": "user",
                "content": f"Customer inquiry:\n{message}\n\nReturn only JSON.",
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)


def resolve_policy(analysis: Dict[str, str]) -> Dict[str, str]:
    """Intermediate business logic: determine SLA and resolution rules based on extracted state."""

    category = analysis.get("category", "general_inquiry")
    urgency = analysis.get("urgency", "medium")

    if category == "billing" and urgency in ("high", "critical"):
        return {
            "sla_response_time": "1 hour",
            "escalation_team": "Priority Billing & Finance Ops",
            "resolution_guidelines": (
                "Acknowledge the billing discrepancy, confirm expedited review with Finance Ops "
                "for refund processing, and provide a direct case tracking reference."
            ),
        }
    elif category == "technical_bug" and urgency in ("high", "critical"):
        return {
            "sla_response_time": "2 hours",
            "escalation_team": "Tier-2 Engineering",
            "resolution_guidelines": (
                "Acknowledge the technical disruption, outline immediate diagnostic steps, "
                "and route logs to Tier-2 Engineering."
            ),
        }
    else:
        return {
            "sla_response_time": "24 hours",
            "escalation_team": "Standard Support",
            "resolution_guidelines": (
                "Provide helpful guidance addressing the customer question and offer links to documentation."
            ),
        }


def draft_reply(
    client: OpenAI,
    model: str,
    message: str,
    analysis: Dict[str, str],
    policy: Dict[str, str],
) -> str:
    """Step 2: Generate a tailored customer reply combining inquiry analysis and resolution policy."""

    context_prompt = dedent(
        f"""
        Customer inquiry:
        {message}

        Case analysis:
        - Category: {analysis.get('category')}
        - Urgency: {analysis.get('urgency')}
        - Customer sentiment: {analysis.get('sentiment')}
        - Core issue: {analysis.get('summary')}

        Resolution policy:
        - Target SLA response: {policy.get('sla_response_time')}
        - Assigned team: {policy.get('escalation_team')}
        - Guidelines: {policy.get('resolution_guidelines')}

        Draft a professional, empathetic 3 to 4 sentence customer reply adhering to the resolution policy.
        """
    ).strip()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise customer support specialist. Write a professional, empathetic reply "
                    "that strictly follows the provided resolution policy and case analysis. "
                    "Do not mention JSON keys or internal system labels."
                ),
            },
            {
                "role": "user",
                "content": context_prompt,
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
        We were double-billed on invoice #INV-9821 for our annual Enterprise tier ($4,800 instead of $2,400).
        This is blocking our quarterly accounting close, and we need an immediate refund and an updated invoice.
        """
    ).strip()

    analysis = analyze_inquiry(client, args.model, message)
    policy = resolve_policy(analysis)
    reply = draft_reply(client, args.model, message, analysis, policy)

    print("=== Prompt chaining support reply ===")
    print("Customer message:")
    print(message)
    print("\nStep 1: extracted analysis")
    print(json.dumps(analysis, indent=2))
    print("\nIntermediate: resolved policy")
    print(json.dumps(policy, indent=2))
    print("\nStep 2: customer reply")
    print(reply)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
