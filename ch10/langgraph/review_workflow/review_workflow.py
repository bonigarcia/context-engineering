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

from typing import TypedDict

from langgraph.graph import END, StateGraph


class ReviewState(TypedDict):
    topic: str
    draft: str
    review: str
    final: str


def draft_node(state: ReviewState) -> dict[str, str]:
    return {"draft": f"Draft answer about {state['topic']}."}


def review_node(state: ReviewState) -> dict[str, str]:
    return {"review": f"Review approved for: {state['draft']}"}


def finalize_node(state: ReviewState) -> dict[str, str]:
    return {"final": f"{state['draft']} | {state['review']}"}


if __name__ == "__main__":
    graph = StateGraph(ReviewState)
    graph.add_node("draft", draft_node)
    graph.add_node("review", review_node)
    graph.add_node("finalize", finalize_node)

    graph.set_entry_point("draft")
    graph.add_edge("draft", "review")
    graph.add_edge("review", "finalize")
    graph.add_edge("finalize", END)

    app = graph.compile()
    result = app.invoke(
        {"topic": "context engineering", "draft": "", "review": "", "final": ""}
    )
    print(result)
