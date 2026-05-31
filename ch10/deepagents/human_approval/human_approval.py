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
from pathlib import Path

try:
    from deepagents import create_deep_agent
except ImportError:  # pragma: no cover - keeps the example importable without deps
    create_deep_agent = None

try:
    from langgraph.checkpoint.memory import MemorySaver
except ImportError:  # pragma: no cover - keeps the example importable without deps
    MemorySaver = None


def remove_file(path: str) -> str:
    target = Path(path)
    if target.exists():
        target.unlink()
        return f"Removed {path}."
    return f"No file found at {path}."


def build_agent():
    if create_deep_agent is None or MemorySaver is None:
        raise RuntimeError("deepagents and langgraph checkpoint support are unavailable; install ../requirements.txt")

    return create_deep_agent(
        model="google_genai:gemini-3.5-flash",
        tools=[remove_file],
        interrupt_on={"remove_file": True},
        checkpointer=MemorySaver(),
    )


def build_output(auto_approve: bool) -> str:
    output = "Awaiting approval for remove_file."
    if auto_approve:
        output += " Approved."
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="DeepAgents human approval demo")
    parser.add_argument("--auto-approve", action="store_true", help="auto-approve the interrupted tool call")
    args = parser.parse_args()

    build_agent()
    print(build_output(args.auto_approve))


if __name__ == "__main__":
    main()
