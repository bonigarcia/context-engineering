import os
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]

class MultiAgentRouter:
    def __init__(self, llm):
        self.llm = llm
        self.graph = self.build_graph()

    def build_graph(self):
        # 1. Define the state graph
        workflow = StateGraph(AgentState)

        # 2. Define the nodes
        workflow.add_node("router", self.router_node)
        workflow.add_node("sales_agent", self.create_agent_node("You are a helpful sales assistant."))
        workflow.add_node("tech_support_agent", self.create_agent_node("You are a helpful technical support assistant."))
        workflow.add_node("general_agent", self.create_agent_node("You are a helpful general assistant."))

        # 3. Define the edges
        workflow.set_entry_point("router")
        workflow.add_conditional_edges(
            "router",
            self.route_question,
            {
                "sales": "sales_agent",
                "tech_support": "tech_support_agent",
                "general": "general_agent",
            },
        )
        workflow.add_edge("sales_agent", END)
        workflow.add_edge("tech_support_agent", END)
        workflow.add_edge("general_agent", END)
        
        # 4. Compile the graph
        return workflow.compile()

    def router_node(self, state):
        # This node doesn't modify the state, it's just for routing
        return state

    def create_agent_node(self, system_prompt):
        """Factory function to create a new agent node."""
        prompt = PromptTemplate(
            template="{system_prompt}\n\nUser Question: {question}",
            input_variables=["system_prompt", "question"],
        )
        def agent_node(state):
            last_message = state["messages"][-1].content
            
            # Invoke the LLM with the specific persona
            response = self.llm.invoke(prompt.format(system_prompt=system_prompt, question=last_message))
            
            return {"messages": [response]}

        return agent_node

    def route_question(self, state):
        """The router function to decide which agent to route to."""
        last_message = state["messages"][-1].content
        
        routing_prompt = f"""You are an expert at routing customer questions.
        Classify the user's question into one of the following categories: 'sales', 'tech_support', or 'general'.
        
        User Question:
        "{last_message}"
        
        Classification:"""
        
        response = self.llm.invoke(routing_prompt)
        # The response will be just the category name, e.g., "sales"
        route = response.content.strip().lower()

        if "sales" in route:
            return "sales"
elif "tech" in route:
            return "tech_support"
        else:
            return "general"

    def run(self, question: str):
        """Run the multi-agent router with a user question."""
        initial_state = {"messages": [HumanMessage(content=question)]}
        final_state = self.graph.invoke(initial_state)
        return final_state['messages'][-1].content

if __name__ == "__main__":
    # Initialize the LLM
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)

    # Create and run the multi-agent router
    router_workflow = MultiAgentRouter(llm)

    # --- Example 1: Sales question ---
    sales_question = "How much does your product cost? I'm interested in a bulk discount."
    print(f"User Question: {sales_question}")
    sales_answer = router_workflow.run(sales_question)
    print(f"Agent Response: {sales_answer}\n")

    # --- Example 2: Tech support question ---
    tech_question = "My application keeps crashing when I try to export a file. Can you help?"
    print(f"User Question: {tech_question}")
    tech_answer = router_workflow.run(tech_question)
    print(f"Agent Response: {tech_answer}\n")

    # --- Example 3: General question ---
    general_question = "What are your business hours?"
    print(f"User Question: {general_question}")
    general_answer = router_workflow.run(general_question)
    print(f"Agent Response: {general_answer}\n")
