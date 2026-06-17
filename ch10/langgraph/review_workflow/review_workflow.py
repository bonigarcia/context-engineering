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

from typing import Literal, TypedDict

from langgraph.graph import END, StateGraph


class GraphState(TypedDict):
    input: str
    draft: str
    needs_review: bool


def draft_answer(state: GraphState) -> dict[str, str]:
    return {
        "draft": "Processed response",
        "needs_review": "payment" in state["input"],
    }


def human_review(state: GraphState) -> dict[str, str]:
    return {"draft": f"Reviewed: {state['draft']}"}


def route_after_draft(state: GraphState) -> Literal["review", "done"]:
    return "review" if state["needs_review"] else "done"


if __name__ == "__main__":
    graph = StateGraph(GraphState)
    graph.add_node("draft", draft_answer)
    graph.add_node("review", human_review)

    graph.set_entry_point("draft")
    graph.add_conditional_edges(
        "draft",
        route_after_draft,
        {"review": "review", "done": END},
    )
    graph.add_edge("review", END)

    app = graph.compile()
    for user_input in ["Summarize the chapter", "Escalate the payment issue"]:
        result = app.invoke({"input": user_input, "draft": "", "needs_review": False})
        print(f"Input: {user_input}")
        print(result)
