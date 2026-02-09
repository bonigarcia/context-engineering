import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent

# Load environment variables from .env file
load_dotenv()

# Check if OPENAI_API_KEY is set
if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# 1. Define a simple tool
def get_current_weather(location: str) -> str:
    """Gets the current weather in a given location."""
    if "london" in location.lower():
        return "It's 15 degrees Celsius and sunny in London."
    elif "paris" in location.lower():
        return "It's 12 degrees Celsius and cloudy in Paris."
    else:
        return "Weather data not available for this location."

weather_tool = FunctionTool.from_defaults(fn=get_current_weather,
                                         description="Get the current weather in a specified location")

# 2. Create some dummy documents and build a VectorStoreIndex
# In a real scenario, these documents would come from various sources
documents = SimpleDirectoryReader(input_files=["data.txt"]).load_data()
index = VectorStoreIndex.from_documents(documents)

# 3. Initialize an OpenAIAgent with a context_retriever and the custom tool
# The context_retriever helps the agent to retrieve relevant information before acting
llm = OpenAI(model="gpt-4")

agent = OpenAIAgent.from_tools(
    tools=[weather_tool],
    llm=llm,
    verbose=True,
    context_retriever=index.as_retriever(),
)

# 4. Demonstrate interactions
print("--- Interaction 1: General knowledge question (should not use tool or RAG) ---")
response = agent.chat("What is the capital of France?")
print(f"Agent: {response}")

print("--- Interaction 2: Question answerable by RAG (should use RAG) ---")
response = agent.chat("What is LlamaIndex?")
print(f"Agent: {response}")

print("--- Interaction 3: Question requiring the tool (should use the weather tool) ---")
response = agent.chat("What's the weather like in London?")
print(f"Agent: {response}")

print("--- Interaction 4: Question not directly covered by RAG or tool ---")
response = agent.chat("Tell me a fun fact about giraffes.")
print(f"Agent: {response}")
