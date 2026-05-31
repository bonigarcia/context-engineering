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

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph


class ResumeState(TypedDict):
    topic: str
    draft: str
    review: str
    final: str


def draft_node(state: ResumeState) -> dict[str, str]:
    return {"draft": f"Draft for {state['topic']}"}


def review_node(state: ResumeState) -> dict[str, str]:
    return {"review": f"Stored review for {state['draft']}"}


def finalize_node(state: ResumeState) -> dict[str, str]:
    return {"final": f"{state['draft']} -> {state['review']}"}


if __name__ == "__main__":
    graph = StateGraph(ResumeState)
    graph.add_node("draft", draft_node)
    graph.add_node("review", review_node)
    graph.add_node("finalize", finalize_node)

    graph.set_entry_point("draft")
    graph.add_edge("draft", "review")
    graph.add_edge("review", "finalize")
    graph.add_edge("finalize", END)

    app = graph.compile(checkpointer=MemorySaver(), interrupt_before=["finalize"])
    config = {"configurable": {"thread_id": "checkpoint-demo"}}

    paused_state = app.invoke(
        {"topic": "checkpointing", "draft": "", "review": "", "final": ""},
        config=config,
    )
    print(f"Paused state: {paused_state}")

    saved_state = app.get_state(config)
    print(f"Persisted state: {saved_state.values}")

    resumed_state = app.invoke({}, config=config)
    print(f"Resumed state: {resumed_state}")
