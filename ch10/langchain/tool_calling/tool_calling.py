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
import datetime

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Define a custom tool
def get_current_time(format: str = "%H:%M:%S") -> str:
    """Returns the current time in the specified format.
    The format should be a string acceptable by datetime.strftime().
    For example: "%H:%M:%S" for hour:minute:second, "%Y-%m-%d" for year-month-day."""
    now = datetime.datetime.now()
    return now.strftime(format)

if __name__ == "__main__":
    # Create the agent
    agent = create_agent(
        model = "gpt-5-mini",
        tools = [get_current_time],
        system_prompt="You are a helpful assistant with access to tools."
    )

    # Invoke the agent with a query that requires tool use
    user_prompt = "What time is it right now?"
    print(f"User: {user_prompt}")
    response = agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
    print(f"Agent response: {response['messages'][-1].content}")
