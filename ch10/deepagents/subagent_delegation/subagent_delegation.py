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

try:
    from deepagents import create_deep_agent
except ImportError:  # pragma: no cover - lets tests monkeypatch the builder
    create_deep_agent = None


def build_agent():
    if create_deep_agent is None:
        raise RuntimeError("deepagents.create_deep_agent is not available")

    subagents = [
        {
            "name": "research-agent",
            "description": "Performs in-depth repository and documentation research.",
            "system_prompt": (
                "Collect only the useful findings, keep notes concise, and avoid "
                "dragging raw source text back into the main context."
            ),
        },
        {
            "name": "writer-agent",
            "description": "Turns research notes into a short final brief.",
            "system_prompt": (
                "Convert the research into a brief summary, and avoid repeating "
                "raw notes or long transcripts."
            ),
        },
    ]

    return create_deep_agent(
        model="openai:gpt-6-luna",
        tools=[],
        subagents=subagents,
        system_prompt=(
            "You are a coordinator. Delegate research and writing through the task tool "
            "to isolated subagents, and keep the main context clean by retaining only "
            "short coordination notes."
        ),
    )


def main() -> None:
    agent = build_agent()
    result = agent.invoke(
        {
            "messages": [
                (
                    "user",
                    "Research the example's delegation pattern and give me a short brief.",
                )
            ]
        }
    )
    print(result)


if __name__ == "__main__":
    main()
