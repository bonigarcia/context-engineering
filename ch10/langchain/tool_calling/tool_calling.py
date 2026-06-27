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
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")


# Define a custom tool
@tool
def lookup_policy(topic: str) -> str:
    """Return the support policy for a topic."""
    return "Refunds above 100 euros require human approval."


if __name__ == "__main__":
    # Initialize the LLM
    llm = ChatOpenAI(api_key=api_key, model="gpt-5-mini", temperature=0)
    llm_with_tools = llm.bind_tools([lookup_policy])

    # Define a chat prompt template with a system message and user input
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Use policy tools when a support answer depends on rules."),
        ("user", "{input}")
    ])

    # Build messages from the prompt
    messages = prompt.invoke({"input": "Can I approve a 250 euro refund?"}).to_messages()

    # Get LLM response (may include tool calls)
    response = llm_with_tools.invoke(messages)

    # Handle tool calls if present
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "lookup_policy":
                result = lookup_policy.invoke(tool_call["args"])
                messages.append(response)
                messages.append(ToolMessage(result, tool_call_id=tool_call["id"]))

        # Invoke again with tool results
        final_response = llm_with_tools.invoke(messages)
        print(final_response.content)
    else:
        print(response.content)
