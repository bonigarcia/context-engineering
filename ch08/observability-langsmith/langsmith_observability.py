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

from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

KNOWLEDGE_BASE = {
    "charged twice": (
        "Billing policy: duplicate charges must be verified by billing before any refund is promised."
    ),
    "reset link": (
        "Support policy: tell the user to request a fresh reset link and avoid claiming the account was restored."
    ),
}


def select_context(question: str) -> str:
    question_lower = question.lower()
    for key, context in KNOWLEDGE_BASE.items():
        if key in question_lower:
            return context
    return "If the policy does not cover the question, escalate to a human reviewer."


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set (env var or .env).")

    if not os.getenv("LANGCHAIN_API_KEY"):
        raise RuntimeError("LANGCHAIN_API_KEY is not set (env var or .env).")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a support assistant. Use the context to answer the question concisely.",
            ),
            (
                "human",
                "Question: {question}\nContext: {context}\nReply in two sentences or fewer.",
            ),
        ]
    )

    chain = (
            {"context": RunnableLambda(select_context), "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    ).with_config(
        tags=["chapter-8", "langsmith"],
        metadata={"chapter": "8", "example": "support-escalation"},
    )

    question = "I was charged twice for order #12345. What should I do?"
    answer = chain.invoke(question)

    print("--- LangSmith traced run ---")
    print(f"Question: {question}")
    print(f"Selected context: {select_context(question)}")
    print(f"Answer: {answer}")
    print(
        "Trace available in LangSmith when LANGSMITH_TRACING=true, LANGCHAIN_PROJECT, and LANGCHAIN_API_KEY are set."
    )


if __name__ == "__main__":
    main()
