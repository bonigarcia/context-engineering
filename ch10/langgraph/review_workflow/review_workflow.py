"""
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from typing import Literal, TypedDict

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, StateGraph

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Initialize the chat model used by the drafting node
model = init_chat_model("openai:gpt-5-mini", temperature=0)


class GraphState(TypedDict):
    input: str
    draft: str
    needs_review: bool


def draft_answer(state: GraphState) -> dict[str, str]:
    # The node calls the model and writes the result into the state
    reply = model.invoke([
        ("system", "Answer the customer request in two sentences."),
        ("user", state["input"]),
    ])
    return {
        "draft": reply.content,
        "needs_review": "payment" in state["input"].lower(),
    }


def human_review(state: GraphState) -> dict[str, str]:
    # A reviewer edits the draft before it reaches the customer
    return {"draft": f"Reviewed: {state['draft']}"}


def route_after_draft(state: GraphState) -> Literal["review", "done"]:
    return "review" if state["needs_review"] else "done"


if __name__ == "__main__":
    # Build and compile the workflow graph
    workflow = StateGraph(GraphState)
    workflow.add_node("draft", draft_answer)
    workflow.add_node("review", human_review)

    workflow.set_entry_point("draft")
    workflow.add_conditional_edges(
        "draft",
        route_after_draft,
        {"review": "review", "done": END},
    )
    workflow.add_edge("review", END)

    app = workflow.compile()
    for user_input in ["Summarize the chapter", "My payment failed twice"]:
        result = app.invoke({"input": user_input})
        print(f"Input: {user_input}")
        print(result)
