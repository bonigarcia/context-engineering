import autogen
import os
import json
from autogen.agentchat import AssistantAgent
from autogen.agentchat.contrib.user_proxy_agent import UserProxyAgent

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Configuration for the models
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

# --- First Interaction ---
print("--- First Interaction: Establishing a preference ---")
assistant_initial = AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. Remember user preferences. Respond with 'TERMINATE' when the task is done.",
)

user_proxy_initial = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
)

user_proxy_initial.initiate_chat(
    assistant_initial,
    message="My favorite color is blue. Can you remember that?",
)

# Save the state of the assistant after the first interaction
saved_state = assistant_initial.save_state()
print(f"--- Saved state of assistant ---{json.dumps(saved_state, indent=2)}")

# --- Second Interaction: Loading state and resuming conversation ---
print("--- Second Interaction: Resuming conversation with restored state ---")
# Create a new assistant instance
assistant_restored = AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. Remember user preferences. Respond with 'TERMINATE' when the task is done.",
)

# Load the previously saved state into the new assistant instance
assistant_restored.load_state(saved_state)

user_proxy_restored = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
)

# Continue the conversation with the restored assistant
user_proxy_restored.initiate_chat(
    assistant_restored,
    message="What is my favorite color?",
)