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
from agno.models.openai import OpenAIResponses
from agno.tools.workspace import Workspace


def build_agent(root: Path) -> Agent:
    return Agent(
        name="Sorting Hat",
        model=OpenAIResponses(id="gpt-5.4-mini"),
        tools=[Workspace(root=str(root), allowed=["read", "list", "search"])],
        instructions=(
            "Inspect the scoped Agno folder, group the files into the companion themes, "
            "and explain how the workspace boundary keeps the agent's context tight. "
            "Also explain why Agno's runtime/control-plane split matters: the agent logic "
            "stays small while AgentOS can later provide storage, traces, and service orchestration."
        ),
        markdown=True,
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    agent = build_agent(root)
    agent.print_response(f"Inventory and organize {root}", stream=True)


if __name__ == "__main__":
    main()
