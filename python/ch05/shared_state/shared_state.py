import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# --- Global State ---
# This simple dictionary acts as the global, shared state for our agents.
document_state = {
    "topic": "The benefits of a 4-day work week",
    "draft_content": "",
    "feedback": "",
    "status": "writing" # Possible statuses: writing, editing, finished
}

def writer_agent(state, llm):
    """
    An agent that writes a draft if the status is 'writing'.
    """
    if state["status"] == "writing":
        print("--- Writer Agent is acting ---")
        
        prompt = f"You are a content writer. Write a short, two-paragraph blog post about the topic: {state['topic']}."
        draft = llm.invoke(prompt).content
        
        # Update the global state
        state["draft_content"] = draft
        state["status"] = "editing"
        print("  - Wrote draft and updated status to 'editing'.\n")
    return state

def editor_agent(state, llm):
    """
    An agent that provides feedback if the status is 'editing'.
    """
    if state["status"] == "editing":
        print("--- Editor Agent is acting ---")
        
        prompt = f"""You are a senior editor. Please provide one concise sentence of feedback on the following draft:

        --- DRAFT ---
        {state['draft_content']}
        --- END DRAFT ---
        
        Your feedback:"""
        feedback = llm.invoke(prompt).content
        
        # Update the global state
        state["feedback"] = feedback
        state["status"] = "finished"
        print("  - Provided feedback and updated status to 'finished'.\n")
    return state

def run_shared_state_collaboration():
    """
    Demonstrates two agents collaborating via shared state in turns.
    """
    # Load environment variables and initialize the LLM
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file or environment.")
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0.7)

    # Use a local variable to manage the state throughout the run.
    # It's initialized from the global state.
    current_state = document_state.copy()

    print("--- Initial Global State ---")
    print(current_state)
    print("-" * 20)

    agents = [writer_agent, editor_agent]
    turn = 0
    max_turns = 5 # A few turns to be safe
    while current_state["status"] != "finished" and turn < max_turns:
        turn += 1
        print(f"\n--- Turn {turn} ---")

        state_before_turn = current_state.copy()

        # Poll each agent once per turn
        for agent_func in agents:
            # Pass the current state to the agent
            current_state = agent_func(current_state, llm)
            # If the agent acted and changed the state, end the turn
            if current_state != state_before_turn:
                break

        # If state hasn't changed after polling all agents, stop.
        if current_state == state_before_turn:
            print("No agent acted this turn. Halting.")
            break

        print(f"--- State after Turn {turn} ---")
        print(current_state)
        print("-" * 20)

    print("\n--- Final Global State ---")
    print(current_state)

if __name__ == "__main__":
    run_shared_state_collaboration()
