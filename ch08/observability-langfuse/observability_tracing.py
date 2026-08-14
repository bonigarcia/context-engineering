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
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from langfuse import get_client
from langfuse.langchain import CallbackHandler

SYSTEM_PROMPT = (
    "Use the available tools to answer questions about programming "
    "languages, and answer concisely."
)

QUESTION = (
    "Who created the Python programming language, and in which year was "
    "it first released?"
)

LANGUAGE_FACTS = {
    "python": "Python was created by Guido van Rossum and first released "
              "in 1991.",
    "java": "Java was created by James Gosling and first released in 1995.",
}


# A deterministic tool keeps the trace reproducible across runs, which matters
# when the trace itself is the thing being inspected
@tool
def lookup_language(name: str) -> str:
    """Look up who created a programming language and when it was first
    released."""
    return LANGUAGE_FACTS.get(name.strip().lower(), f"No record for {name}.")


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
    tools = [lookup_language]

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
