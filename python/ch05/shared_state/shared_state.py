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
    Demonstrates two agents collaborating via shared global state.
    """
    # Load environment variables and initialize the LLM
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file or environment.")
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0.7)

    print("--- Initial Global State ---")
    print(document_state)
    print("-" * 20)

    # The orchestrator calls the agents in sequence.
    # Each agent checks the global state to decide whether to act.
    
    # Call 1: Writer acts, Editor does nothing
    global document_state
    document_state = writer_agent(document_state, llm)
    document_state = editor_agent(document_state, llm)
    
    print("--- State after first round ---")
    print(document_state)
    print("-" * 20)

    # Call 2: Writer does nothing, Editor acts
    document_state = writer_agent(document_state, llm)
    document_state = editor_agent(document_state, llm)

    print("--- Final Global State ---")
    print(document_state)

if __name__ == "__main__":
    run_shared_state_collaboration()
