import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def run_stateful_loop():
    """
    Simple, stateful agent loop.
    """
    # Load environment variables and initialize the LLM
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file or environment.")
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)

    # 1. Initialize the state
    agent_state = {
        "topic": "The role of context engineering in AI",
        "research_summary": "",
        "iteration_count": 0,
        "max_iterations": 3
    }
    print(f"--- Initial State ---\n{agent_state}\n")

    # 2. Run the agent loop
    while agent_state["iteration_count"] < agent_state["max_iterations"]:
        agent_state["iteration_count"] += 1
        print(f"--- Iteration {agent_state['iteration_count']} ---")

        # Prepare the prompt based on the current state
        if agent_state["iteration_count"] == 1:
            # First iteration: Generate an initial summary
            prompt = f"You are a research assistant. Generate a brief, one-paragraph summary about the topic: {agent_state['topic']}."
        else:
            # Subsequent iterations: Refine the summary
            prompt = f"""You are a research assistant. Your current summary is:
            '{agent_state['research_summary']}'
            Based on this, what is a key sub-topic or question worth exploring next to deepen the research?
            Please provide a single, concise sentence describing the next research direction."""

        # Call the LLM
        response = llm.invoke(prompt)
        new_information = response.content

        # 3. Update the state
        if agent_state["iteration_count"] == 1:
            agent_state["research_summary"] = new_information
            print(f"  Action: Generated initial summary.")
        else:
            # In a more complex agent, you'd do more with this, but here we just append it.
            agent_state["research_summary"] += f"\n\nNext step: {new_information}"
            print(f"  Action: Identified next research step.")
        
        print(f"  New Summary: \"{agent_state['research_summary'][:100]}...\"\n")

    print(f"--- Final State ---\n{agent_state}")

if __name__ == "__main__":
    run_stateful_loop()