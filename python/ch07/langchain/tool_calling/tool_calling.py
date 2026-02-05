import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain import hub
import datetime

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Define a custom tool
@tool
def get_current_time(format: str = "%H:%M:%S") -> str:
    """Returns the current time in the specified format.
    The format should be a string acceptable by datetime.strftime().
    For example: "%H:%M:%S" for hour:minute:second, "%Y-%m-%d" for year-month-day."""
    now = datetime.datetime.now()
    return now.strftime(format)

if __name__ == "__main__":
    # Initialize the LLM
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)

    # Define the tools available to the agent
    tools = [get_current_time]

    # Get the Agent Prompt from LangChain Hub
    # This prompt is designed for tool-calling agents
    prompt = hub.pull("hwchase17/openai-functions-agent")

    # Create the agent using create_tool_calling_agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create an agent executor to run the agent
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Invoke the agent with a query that requires tool use
    print("--- Query 1: Get current time ---")
    response1 = agent_executor.invoke({"input": "What time is it right now?"})
    print(f"Agent response: {response1['output']}")

    print("--- Query 2: Get current date in a specific format ---")
    response2 = agent_executor.invoke({"input": "What is today's date in YYYY-MM-DD format?"})
    print(f"Agent response: {response2['output']}")

    print("--- Query 3: A simple question not requiring tools ---")
    response3 = agent_executor.invoke({"input": "What is the capital of Spain?"})
    print(f"Agent response: {response3['output']}")
