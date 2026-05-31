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
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Define a simple custom tool
def get_current_weather(city: str) -> str:
    """Returns the current weather in a given city."""
    if city == "London":
        return "The weather in London is cloudy with a temperature of 10°C."
    elif city == "Paris":
        return "The weather in Paris is sunny with a temperature of 15°C."
    else:
        return "I don't have weather information for that city."

# Convert the Python function to a LlamaIndex tool
weather_tool = FunctionTool.from_defaults(fn=get_current_weather)

# Initialize the LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.0)

# Create an agent with the tool
agent = FunctionAgent(tools=[weather_tool], llm=llm)


async def main():
    # Interact with the agent
    print("Agent: Hello! I can tell you the weather. What city are you interested in?")

    response = await agent.run("What is the weather in London?")
    print(f"User: What is the weather in London?")
    print(f"Agent: {response}")

    response = await agent.run("How about Berlin?")
    print(f"User: How about Berlin?")
    print(f"Agent: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

