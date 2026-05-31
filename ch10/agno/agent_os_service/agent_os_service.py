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
from agno.os import AgentOS
from fastapi import FastAPI


def build_agent(root: Path) -> Agent:
    return Agent(
        name="AgentOS Service Agent",
        model=OpenAIResponses(id="gpt-5.4-mini"),
        markdown=True,
        instructions=(
            "Describe the difference between the runtime agent and the AgentOS control plane, "
            "using the local companion folder as the concrete example."
        ),
        add_datetime_to_context=True,
    )


def build_os(root: Path) -> AgentOS:
    return AgentOS(
        name="AgentOS Service",
        description="Minimal AgentOS service for the Chapter 10 Agno example.",
        agents=[build_agent(root)],
    )


def build_app(root: Path) -> FastAPI:
    return build_os(root).get_app()


def main() -> None:
    root = Path(__file__).resolve().parent
    os = build_os(root)
    app = os.get_app()
    os.serve(app, host="127.0.0.1", port=7777, reload=False)


if __name__ == "__main__":
    main()
