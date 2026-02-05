import os
from llama_index.core.agent import AgentRunner
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.llms.openai import OpenAI # Import for LLM

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

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
agent = AgentRunner(tools=[weather_tool], llm=llm)

# Interact with the agent
print("Agent: Hello! I can tell you the weather. What city are you interested in?")

response = agent.chat("What is the weather in London?")
print(f"User: What is the weather in London?")
print(f"Agent: {response}")

response = agent.chat("How about Berlin?")
print(f"User: How about Berlin?")
print(f"Agent: {response}")

