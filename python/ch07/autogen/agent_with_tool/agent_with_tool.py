import autogen
import os

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Configuration for the models
config_list = [
    {
        "model": "gpt-4", # You can change this to gpt-3.5-turbo if you don't have GPT-4 access
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

# Define a simple tool function
def calculate_square(number: int) -> int:
    """
    Calculates the square of a given number.
    """
    return number * number

# Create an AssistantAgent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. You can use available tools to answer questions. Respond with 'TERMINATE' when the task is done.",
)

# Create a UserProxyAgent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
    # Register the tool function
    function_map={"calculate_square": calculate_square}
)

# Start the conversation
user_proxy.initiate_chat(
    assistant,
    message="What is the square of 15? Use the calculate_square tool.",
)