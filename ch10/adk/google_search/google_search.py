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

from google.adk.agents.llm_agent import Agent
from google.genai.types import Content, Part
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

APP_NAME = "google_search_agent_app"
USER_ID = "user1"
SESSION_ID = "session1"
MODEL = "gemini-3.5-flash"

async def main():
    # Define the agent with the Google Search tool
    search_agent = Agent(
        model=MODEL,
        name="SearchAgent",
        instruction="You are a helpful assistant that can answer questions by searching the web. Use the 'GoogleSearchTool' if you need to find information online.",
        tools=[google_search],
    )

    session_service = InMemorySessionService()
    runner = Runner(
        agent=search_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    print("Agent is ready. Type your questions. Type 'quit' to exit.")

    while True:
        user_input = input("You > ")
        if user_input.lower() == 'quit':
            break

        user_message = Content(parts=[Part(text=user_input)], role="user")
        
        final_response_text = ""
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=user_message):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text # Assuming first part is text
        
        print(f"Agent: {final_response_text}")

if __name__ == "__main__":
    asyncio.run(main())
