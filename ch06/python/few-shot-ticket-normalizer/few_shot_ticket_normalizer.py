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
from typing import Dict, List

from openai import OpenAI


DEFAULT_MODEL = os.getenv("MODEL", "gpt-4o-mini")


def build_messages(report: str) -> List[Dict[str, str]]:
    """Create a few-shot conversation that teaches the output schema."""

    return [
        {
            "role": "system",
            "content": (
                "You normalize bug reports into compact support tickets. "
                "Return only valid JSON with the keys title, category, priority, summary, and next_step."
            ),
        },
        {
            "role": "user",
            "content": (
                "Bug report:\n"
                "The mobile app crashes when I try to upload a 20 MB PDF. It worked yesterday."
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "title": "Crash when uploading large PDF",
                    "category": "file_upload",
                    "priority": "high",
                    "summary": "The mobile app crashes during PDF upload when the file is around 20 MB.",
                    "next_step": "Investigate upload limits and crash logs for the mobile client.",
                },
                indent=2,
            ),
        },
        {
            "role": "user",
            "content": (
                "Bug report:\n"
                "Search results on the dashboard take a long time to load, especially in the morning."
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "title": "Slow dashboard search",
                    "category": "performance",
                    "priority": "medium",
                    "summary": "Dashboard search becomes slow, with the issue being most visible during morning usage.",
                    "next_step": "Check query latency, indexing, and peak-time load on the search service.",
                },
                indent=2,
            ),
        },
        {
            "role": "user",
            "content": f"Bug report:\n{report}\n\nReturn only JSON.",
        },
    ]


def normalize_report(client: OpenAI, model: str, report: str) -> Dict[str, str]:
    response = client.chat.completions.create(
        model=model,
        messages=build_messages(report),
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Few-shot ticket normalizer")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set")

    client = OpenAI()
    report = dedent(
        """
        The app logs me out whenever I close the browser tab.
        I already checked the password manager, and I have to sign in every time.
        """
    ).strip()

    ticket = normalize_report(client, args.model, report)

    print("=== Few-shot ticket normalizer ===")
    print("Bug report:")
    print(report)
    print("\nNormalized ticket:")
    print(json.dumps(ticket, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
