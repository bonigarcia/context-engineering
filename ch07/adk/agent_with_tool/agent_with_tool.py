from google.adk.agents.llm_agent import Agent
from google.genai.types import Content, Part
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

APP_NAME = "agent_with_tool_app"
USER_ID = "user1"
SESSION_ID = "session1"
MODEL = "gemini-2.0-flash"

# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

async def main():
    # Define the agent with a custom tool
    my_agent = Agent(
        model=MODEL,
        name='my_agent',
        instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
        tools=[get_current_time],
    )

    session_service = InMemorySessionService()
    runner = Runner(
        agent=my_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    user_prompt = "What is the time in Madrid?"
    user_message = Content(parts=[Part(text=user_prompt)], role="user")
        
    response = ""
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=user_message):
        if event.is_final_response() and event.content and event.content.parts:
            response = event.content.parts[0].text

    print(f"User: {user_prompt}")
    print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())
