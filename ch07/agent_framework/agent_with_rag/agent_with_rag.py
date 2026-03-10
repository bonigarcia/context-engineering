import asyncio
import importlib
import os
from dataclasses import dataclass
from typing import Annotated, Optional, Sequence

from dotenv import load_dotenv

import agent_framework
from agent_framework.openai import OpenAIResponsesClient

from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding
from semantic_kernel.connectors.in_memory import InMemoryCollection
from semantic_kernel.data.vector import VectorStoreField, vectorstoremodel
from semantic_kernel.functions import KernelParameterMetadata


# =============
# CONFIGURATION
# =============
CHAT_MODEL_ID = "gpt-4o-mini"
EMBEDDING_MODEL_ID = "text-embedding-3-small"
EMBEDDING_DIMS = 1536  # text-embedding-3-small


# ===============
# Agent Framework
# ===============
def _resolve_tool_wrapper_class():
    """
    In some Agent Framework package layouts, the underlying class is not exported at the package root,
    and may live in different modules (or be renamed to FunctionTool).

    This function tries multiple known locations and returns the class object.
    """
    # (module, attribute)
    candidates = [
        ("agent_framework", "AIFunction"),
        ("agent_framework", "FunctionTool"),
        ("agent_framework.aifunction", "AIFunction"),
        ("agent_framework.ai_function", "AIFunction"),
        ("agent_framework.function_tool", "FunctionTool"),
        ("agent_framework.core", "AIFunction"),
        ("agent_framework.core", "FunctionTool"),
        ("agent_framework.core.ai_function", "AIFunction"),
    ]

    for mod_name, attr in candidates:
        try:
            mod = importlib.import_module(mod_name)
            if hasattr(mod, attr):
                return getattr(mod, attr), attr
        except ModuleNotFoundError:
            continue

    raise ImportError(
        "Could not locate Agent Framework tool wrapper class (AIFunction/FunctionTool). "
        "Tried common module paths but none were present."
    )


# Ensure agent_framework.AIFunction exists for Semantic Kernel bridging
if not hasattr(agent_framework, "AIFunction"):
    tool_cls, found_name = _resolve_tool_wrapper_class()
    # If the class is FunctionTool in this install, alias it as AIFunction for SK compatibility
    setattr(agent_framework, "AIFunction", tool_cls)


# ==========================
# Vector Store Model
# ==========================
@vectorstoremodel
@dataclass
class SupportArticle:
    article_id: Annotated[str, VectorStoreField("key")]

    title: Annotated[str, VectorStoreField("data", is_indexed=True, is_full_text_indexed=True)]
    category: Annotated[str, VectorStoreField("data", is_indexed=True, is_full_text_indexed=True)]
    content: Annotated[str, VectorStoreField("data", is_indexed=True, is_full_text_indexed=True)]

    vector: Annotated[
        Optional[list[float] | str],
        VectorStoreField(
            "vector",
            dimensions=EMBEDDING_DIMS,
            distance_function="cosine_similarity",
            embedding_generator=OpenAITextEmbedding(ai_model_id=EMBEDDING_MODEL_ID),
        ),
    ] = None

    def __post_init__(self) -> None:
        if self.vector is None:
            self.vector = (
                f"Title: {self.title}\n"
                f"Category: {self.category}\n"
                f"Content: {self.content}"
            )


def build_sample_articles() -> list[SupportArticle]:
    return [
        SupportArticle(
            article_id="policy-returns",
            title="Return Policy",
            category="returns",
            content=(
                "Customers may return items within 30 days of delivery. "
                "Items must be unused and in original packaging. "
                "Refunds are issued within 5 business days after inspection."
            ),
        ),
        SupportArticle(
            article_id="policy-shipping",
            title="Shipping Information",
            category="shipping",
            content=(
                "Standard shipping takes 3–5 business days. "
                "Orders over $50 qualify for free standard shipping. "
                "Expedited shipping is available."
            ),
        ),
        SupportArticle(
            article_id="policy-warranty",
            title="Warranty Coverage",
            category="warranty",
            content=(
                "Products include a limited 1-year warranty covering manufacturing defects. "
                "Proof of purchase is required for claims."
            ),
        ),
    ]


async def upsert_records(collection: InMemoryCollection, records: Sequence[SupportArticle]) -> None:
    """
    Tolerate minor SK API drift:
    - Prefer upsert_batch(records)
    - Fall back to upsert(records) or upsert(record)
    """
    if hasattr(collection, "upsert_batch"):
        await collection.upsert_batch(list(records))
        return

    if hasattr(collection, "upsert"):
        try:
            await collection.upsert(list(records))
            return
        except TypeError:
            for r in records:
                await collection.upsert(r)
            return

    raise RuntimeError("Collection has no supported upsert method (expected upsert_batch or upsert).")


async def main() -> None:
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Please set OPENAI_API_KEY in your environment (or .env).")

    # Set model id programmatically
    os.environ["OPENAI_RESPONSES_MODEL_ID"] = CHAT_MODEL_ID

    # Build in-memory vector KB
    collection = InMemoryCollection(
        record_type=SupportArticle,
        collection_name="support_articles",
    )

    await upsert_records(collection, build_sample_articles())

    # In-memory connector does NOT support hybrid; use vector search.
    search_function = collection.create_search_function(
        function_name="search_knowledge_base",
        description="Search the support knowledge base for policy/procedure information.",
        search_type="vector",
        parameters=[
            KernelParameterMetadata(
                name="query",
                description="Search query to find relevant information.",
                type="str",
                is_required=True,
                type_object=str,
            ),
            KernelParameterMetadata(
                name="top",
                description="Number of results to return.",
                type="int",
                default_value=3,
                type_object=int,
            ),
        ],
        string_mapper=lambda x: (
            f"[{x.record.category}] {x.record.title}\n"
            f"{x.record.content}\n"
            f"SourceId: {x.record.article_id}"
        ),
    )

    # Bridge SK search function into an Agent Framework tool
    search_tool = search_function.as_agent_framework_tool()

    # Create the agent
    client = OpenAIResponsesClient()
    agent = client.as_agent(
        instructions=(
            "You are a helpful support assistant. "
            "Use the search tool before answering. "
            "If you use retrieved information, cite SourceId(s) explicitly."
        ),
        tools=search_tool,
    )

    print("\nAgent ready. Ask a question (type 'exit' to quit).\n")

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break

        response = await agent.run(question)
        print(f"\nAgent: {response.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
