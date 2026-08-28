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

import asyncio

from claude_agent_sdk import ClaudeAgentOptions, query


async def main() -> None:
    # The harness defaults are set once, before the loop starts
    options = ClaudeAgentOptions(
        system_prompt="You are a concise assistant for research tasks.",
        allowed_tools=["Read", "Grep", "Write"],
        permission_mode="acceptEdits",
        max_turns=3,
    )

    # The SDK runs the agent loop and streams the resulting messages
    async for message in query(
        prompt="Summarize the README files in three bullets.",
        options=options,
    ):
        print(message)


if __name__ == "__main__":
    asyncio.run(main())
