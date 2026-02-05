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

# Create an AssistantAgent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. You can write and execute Python code to solve problems. Respond with 'TERMINATE' when the task is done.",
)

# Create a UserProxyAgent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER", # Set to "ALWAYS" to allow human intervention
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding", # Agents can write code in this directory
        "use_docker": False, # Set to True to execute code in a Docker container for safety
    },
)

# Start the conversation
user_proxy.initiate_chat(
    assistant,
    message="What is the 10th Fibonacci number? Write and execute Python code to find it.",
)