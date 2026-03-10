import autogen
import os

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Configuration for the models
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. Your goal is to help the user write a simple Python script. Respond with 'TERMINATE' when the task is done.",
)

# Configure UserProxyAgent to always ask for human input
user_proxy_hitl = autogen.UserProxyAgent(
    name="user_proxy_hitl",
    human_input_mode="ALWAYS", # Human intervention is always requested
    max_consecutive_auto_reply=0, # Assistant waits for human input after each reply
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
)

user_proxy_hitl.initiate_chat(
    assistant,
    message="Propose a plan to write a simple Python script that calculates the factorial of a number.",
)