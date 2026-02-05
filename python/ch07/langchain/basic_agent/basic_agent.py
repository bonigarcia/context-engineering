import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
import operator

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
    output: Annotated[str, operator.add]

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

def end_node(state: GraphState):
    """
    Node that represents the end of the graph, simply passes the state.
    """
    print("---END_NODE---")
    return state

if __name__ == "__main__":
    # Build the graph
    workflow = StateGraph(GraphState)

    workflow.add_node("llm_node", call_llm)
    workflow.add_node("final_output", end_node)

    # Set up edges
    workflow.set_entry_point("llm_node")
    workflow.add_edge("llm_node", "final_output")
    workflow.add_edge("final_output", END)

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