"""Deterministic streaming example for Pydantic AI."""

import asyncio
from collections.abc import AsyncIterator

from pydantic_ai import Agent, ModelMessage
from pydantic_ai.models.function import AgentInfo, FunctionModel


step_agent = Agent(
    "openai:gpt-4o-mini",
    instructions="Answer in three short steps and keep the response concise.",
)


async def stepwise_stream(
    messages: list[ModelMessage], info: AgentInfo
) -> AsyncIterator[str]:
    del messages, info
    yield "Step 1: Read the ticket.\n"
    await asyncio.sleep(0)
    yield "Step 2: Check the queue rules.\n"
    await asyncio.sleep(0)
    yield "Step 3: Route the ticket and confirm.\n"


async def main() -> None:
    with step_agent.override(model=FunctionModel(stream_function=stepwise_stream)):
        async with step_agent.run_stream(
            "Give me a stepwise triage plan for a broken checkout flow."
        ) as result:
            async for chunk in result.stream_output():
                print(chunk, end="")


if __name__ == "__main__":
    asyncio.run(main())
