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
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

if __name__ == "__main__":
    # Initialize the LLM
    llm = ChatOpenAI(api_key=api_key, model="gpt-5-mini", temperature=0)

    # Short-term memory is provided by a checkpointer, which stores the
    # message history of every conversation thread. InMemorySaver keeps that
    # history in the process, and a persistent saver would be used in
    # production. This mechanism replaces the legacy ConversationBufferMemory
    # class, which is now part of langchain-classic
    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt="You are a helpful AI assistant.",
        checkpointer=InMemorySaver(),
    )

    # Every turn shares the same thread identifier, so the agent reloads the
    # accumulated history instead of receiving it in the prompt
    thread_config = {"configurable": {"thread_id": "conversation-1"}}

    turns = [
        "Hi there! What's your name?",
        "What did I just ask you?",
        "And what is your name again?",
    ]

    # Simulate a conversation
    for index, user_input in enumerate(turns, start=1):
        print(f"--- Conversation Turn {index} ---")
        state = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            thread_config,
        )
        print(f"User: {user_input}")
        print(f"AI: {state['messages'][-1].content}")
        print(f"Current History: {state['messages']}")
