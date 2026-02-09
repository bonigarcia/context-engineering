from google.adk.agents.llm_agent import Agent
from google.genai.types import Content, Part
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

APP_NAME = "basic_agent"
USER_ID = "user1"
SESSION_ID = "session1"
MODEL = "gemini-2.0-flash"


async def main():
    # Define the agent
    my_agent = Agent(
        model=MODEL,
        name='my_agent',
        instruction="You are a helpful assistant.",
    )

    session_service = InMemorySessionService()
    runner = Runner(
        agent=my_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    user_prompt = "Hello, agent!"
    user_message = Content(parts=[Part(text=user_prompt)], role="user")
        
    response = ""
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=user_message):
        if event.is_final_response() and event.content and event.content.parts:
            response = event.content.parts[0].text

    print(f"User: {user_prompt}")
    print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())
