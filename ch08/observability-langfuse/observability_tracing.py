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
import uuid

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

from langfuse import get_client
from langfuse.langchain import CallbackHandler

SYSTEM_PROMPT = (
    "You are a helpful assistant. Use the available tools whenever the "
    "answer depends on information you do not already have. When you have "
    "the final answer, respond concisely."
)

QUESTION = (
    "Identify who created the Python programming language and the year of "
    "its first release."
)


def _ensure_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise ValueError(f"{name} must be set (environment or .env).")
    return val


def main():
    load_dotenv()

    _ensure_env("OPENAI_API_KEY")
    _ensure_env("LANGFUSE_PUBLIC_KEY")
    _ensure_env("LANGFUSE_SECRET_KEY")
    # LANGFUSE_HOST is optional, and it is only needed for self-hosted servers

    # Langfuse client (used later to build the trace URL) and callback handler
    langfuse_client = get_client()
    langfuse_handler = CallbackHandler()

    # Model and tools
    llm = ChatOpenAI(
        model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY")
    )
    tools = [DuckDuckGoSearchRun()]

    agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)

    print("--- Running agent with Langfuse tracing ---")

    # A trace identifier is generated in advance so the run can be located
    # later in the Langfuse UI
    trace_id = str(uuid.uuid4())

    response = agent.invoke(
        {"messages": [{"role": "user", "content": QUESTION}]},
        config={"callbacks": [langfuse_handler], "run_id": trace_id},
    )

    # The agent returns the full message list, and the answer is the content
    # of the last message
    final_answer = response["messages"][-1].content

    # Flush queued events, which matters in short-lived scripts
    langfuse_client.flush()

    print("\n--- Trace ---")
    try:
        trace_url = langfuse_client.get_trace_url(trace_id=trace_id)
        print(f"View the trace in Langfuse: {trace_url}")
    except Exception:
        print(f"Trace created with trace_id={trace_id} (URL unavailable).")

    print("\n--- Final Answer ---")
    print(final_answer)


if __name__ == "__main__":
    main()
