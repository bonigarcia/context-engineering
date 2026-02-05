import autogen
import os

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Configuration for the models
config_list = [
    {
        "model": "gpt-4",  # You can change this to gpt-3.5-turbo if you don't have GPT-4 access
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

# Create a RAG agent (AssistantAgent with RAG capabilities)
# For simplicity, we will use a UserProxyAgent to simulate RAG by feeding the context
# In a real scenario, you would integrate with a vector database and retrieval mechanism
# using a tool or a custom agent.

# For a simpler example focusing on how AutoGen handles external knowledge as context:
# We'll use a UserProxyAgent to read the document and provide it as context to the AssistantAgent.

# Define the data file
DATA_FILE = "data.txt"

# Create an AssistantAgent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. Answer questions based on the provided information. Respond with 'TERMINATE' when the task is done.",
)

# Create a UserProxyAgent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

# Read the external data
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, DATA_FILE)
with open(data_path, "r") as f:
    knowledge_base = f.read()

# Start the conversation with the knowledge base as context
user_proxy.initiate_chat(
    assistant,
    message=f"Here is some information: {knowledge_base} Based on this information, what is AutoGen?",
)
