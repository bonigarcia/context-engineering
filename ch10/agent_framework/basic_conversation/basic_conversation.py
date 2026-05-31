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
from agent_framework.openai import OpenAIChatClient

async def main():
    # Create client
    client = OpenAIChatClient(model_id="gpt-5")

    # Agent creation with factory method
    agent = client.as_agent(
        name="assistant",
        instructions="You are a helpful assistant.",
    )

    # User prompt
    user_prompt = "What is the size of your context window"
    response = await agent.run(user_prompt)
    print(f"User: {user_prompt}")
    print(f"Agent response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
