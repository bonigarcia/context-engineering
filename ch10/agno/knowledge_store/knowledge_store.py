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

from pathlib import Path

from agno.agent import Agent
from agno.knowledge import FileSystemKnowledge
from agno.models.openai import OpenAIResponses


def build_knowledge(root: Path) -> FileSystemKnowledge:
    return FileSystemKnowledge(
        base_dir=str(root),
        max_results=3,
        include_patterns=["README.md", "*.py"],
    )


def build_agent(root: Path) -> Agent:
    return Agent(
        name="Knowledge Store",
        model=OpenAIResponses(id="gpt-5.4-mini"),
        knowledge=build_knowledge(root),
        add_knowledge_to_context=True,
        markdown=True,
        instructions=(
            "Use the attached knowledge store to answer questions about the local example "
            "files, and explain that knowledge is an explicit runtime input."
        ),
    )


def main() -> None:
    root = Path(__file__).resolve().parent
    agent = build_agent(root)
    agent.print_response(
        "What does this knowledge store example know about the local companion files?",
        stream=True,
    )


if __name__ == "__main__":
    main()
