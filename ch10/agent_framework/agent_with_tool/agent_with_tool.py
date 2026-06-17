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
from agent_framework import tool
from agent_framework.openai import OpenAIChatClient

# Create simple tools for the example
@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: sunny"

@tool
def get_time() -> str:
    """Get current time."""
    return "Current time: 2:30 PM"

async def main():
    # Create client
    client = OpenAIChatClient(model="gpt-5-mini")

    # Agent creation with factory method
    agent = client.as_agent(
        name="assistant",
        instructions="You are a helpful assistant.",
    )

    # Execution with runtime tool and options configuration
    user_prompt = "What's the weather in Madrid?"
    response = await agent.run(
        user_prompt,
        tools=[get_weather, get_time],
        options={"tool_choice": "auto"}
    )
    print(f"User: {user_prompt}")
    print(f"Agent response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
