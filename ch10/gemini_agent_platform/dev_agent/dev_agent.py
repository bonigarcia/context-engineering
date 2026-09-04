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
from google.adk.tools import FunctionTool
from vertexai import agent_engines

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
STAGING_BUCKET = os.getenv("STAGING_BUCKET")


def read_spec(path: str) -> str:
    """Read a spec file from the local filesystem."""
    with open(path) as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    with open(path, "w") as f:
        f.write(content)
    return f"Written to {path}"


async def main() -> None:
    client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

    agent = Agent(
        model="gemini-3.5-flash",
        name="dev_agent",
        instruction=(
            "You are a development agent. When given a feature description:\n"
            "1. Read the spec file to understand the requirements.\n"
            "2. Create a brief implementation plan.\n"
            "3. Write the implementation code.\n"
            "4. Write tests that verify correctness.\n"
            "Use the read_spec and write_file tools to interact with files."
        ),
        tools=[
            FunctionTool(func=read_spec),
            FunctionTool(func=write_file),
        ],
    )
    app = agent_engines.AdkApp(agent=agent)

    remote_agent = client.agent_engines.create(
        agent=app,
        config={
            "requirements": ["google-cloud-aiplatform[agent_engines,adk]"],
            "staging_bucket": STAGING_BUCKET,
        },
    )

    async for event in remote_agent.async_stream_query(
        user_id="user1",
        message="Implement the feature described in spec.md and write tests for it.",
    ):
        print(event)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())