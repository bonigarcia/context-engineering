from agent_framework import ChatAgent, tool
from agent_framework.openai import OpenAIChatClient
import asyncio

# Create simple tools for the example
@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: sunny"

@tool
def get_time() -> str:
    """Get current time."""
    return "Current time: 2:30 PM"

# Create client
client = OpenAIChatClient(model_id="gpt-5")

async def main():
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