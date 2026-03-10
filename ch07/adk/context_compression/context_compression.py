from google.adk.agents.llm_agent import Agent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

APP_NAME = "basic_agent"
USER_ID = "user1"
SESSION_ID = "session1"
MODEL = "gemini-2.0-flash"


async def main():
    root_agent = Agent(
        model=MODEL,
        name="my_agent",
        instruction="You are a helpful assistant.",
    )

    summarizer = LlmEventSummarizer(llm=Gemini(model=MODEL))

    app = App(
        name=APP_NAME,
        root_agent=root_agent,
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=3,  # summarize every 3 invocations
            overlap_size=1,
            summarizer=summarizer,
        ),
    )

    # Session service
    session_service = InMemorySessionService()

    runner = Runner(
        app=app,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Create the session once
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    prompts = [
        "Hello, agent!",
        "Tell me a fun fact.",
        "What did I ask you so far?"
    ]

    for user_prompt in prompts:
        user_message = Content(parts=[Part(text=user_prompt)], role="user")

        response_text = ""
        async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=user_message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text

        print(f"User:  {user_prompt}")
        print(f"Agent: {response_text}\n")


if __name__ == "__main__":
    asyncio.run(main())