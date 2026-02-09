import asyncio
from agent_framework import ChatAgent, tool
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