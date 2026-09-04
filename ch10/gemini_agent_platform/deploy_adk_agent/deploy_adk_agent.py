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

import os

import vertexai
from google.adk.agents import Agent
from vertexai import agent_engines

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
STAGING_BUCKET = os.getenv("STAGING_BUCKET")


async def main() -> None:
    client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

    # A local ADK agent becomes the payload for the managed runtime
    agent = Agent(
        model="gemini-3.5-flash",
        name="context_assistant",
        instruction="You are a helpful assistant.",
    )
    app = agent_engines.AdkApp(agent=agent)

    # The service hosts the agent together with managed sessions
    remote_agent = client.agent_engines.create(
        agent=app,
        config={
            "requirements": ["google-cloud-aiplatform[agent_engines,adk]"],
            "staging_bucket": STAGING_BUCKET,
        },
    )

    async for event in remote_agent.async_stream_query(
        user_id="user1",
        message="What is context engineering?",
    ):
        print(event)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
