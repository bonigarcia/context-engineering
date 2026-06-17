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

import os

try:
    from deepagents import create_deep_agent
except ImportError:  # pragma: no cover - lets tests monkeypatch the builder
    create_deep_agent = None


def main() -> None:
    # 1. Create a DeepAgent
    # DeepAgents are designed for long-horizon tasks with built-in planning and filesystem context
    # The virtual filesystem is enabled by default, providing tools like ls, read_file, and write_file.
    if create_deep_agent is None:
        raise RuntimeError("deepagents.create_deep_agent is not available")

    agent = create_deep_agent(
        model="openai:gpt-5-mini",  # Replace with your preferred model
        tools=[],  # Add custom tools here; built-in filesystem tools are included by default
        system_prompt="You are a senior analyst capable of complex research and planning."
    )

    # 2. Define a complex task
    # DeepAgents will automatically use the 'write_todos' tool to create a plan
    user_request = "Research the latest trends in context engineering for 2026 and save a report.md"

    print(f"Executing task: {user_request}")

    # 3. Invoke the agent
    # The orchestration layer handles task decomposition, sub-agent spawning, and state management
    result = agent.invoke({"messages": [("user", user_request)]})

    # 4. Display the results from the virtual filesystem
    if os.path.exists("report.md"):
        print("\nReport generated successfully in virtual filesystem:")
        with open("report.md", "r", encoding="utf-8") as f:
            print(f.read()[:200] + "...")
    else:
        print("\nTask complete. (Note: Running this in a real environment requires API keys)")

    # 5. Inspect the plan (todos) generated during execution
    # DeepAgents maintain an explicit plan that evolves as the task progresses
    # This is a core part of context orchestration in this framework
    print("\nFinal execution state (message list) contains the plan and sub-agent results.")


if __name__ == "__main__":
    main()
