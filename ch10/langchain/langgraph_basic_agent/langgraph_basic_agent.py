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
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Define our graph state
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        input: User input
        output: LLM output
    """
    input: str
    output: str

# Define the nodes
def call_llm(state: GraphState):
    """
    Node that calls the LLM to generate a response based on the input.
    """
    print("---CALL_LLM---")
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("user", "{input}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"input": state["input"]})
    return {"output": response}

if __name__ == "__main__":
    # Build the graph
    workflow = StateGraph(GraphState)

    workflow.add_node("llm_node", call_llm)

    # Set up edges
    workflow.set_entry_point("llm_node")
    workflow.add_edge("llm_node", END)

    # Compile the graph
    app = workflow.compile()

    # Invoke the graph
    initial_state = {"input": "Hello, how are you today?", "output": ""}
    final_state = app.invoke(initial_state)

    print(f"Initial Input: {initial_state['input']}")
    print(f"Final Output: {final_state['output']}")

    initial_state_2 = {"input": "What is the capital of France?", "output": ""}
    final_state_2 = app.invoke(initial_state_2)

    print(f"Initial Input 2: {initial_state_2['input']}")
    print(f"Final Output 2: {final_state_2['output']}")
