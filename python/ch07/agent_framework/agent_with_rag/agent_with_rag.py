import asyncio
import os
from typing import List

from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding
from semantic_kernel.connectors.azure_ai_search import AzureAISearchCollection
from semantic_kernel.functions import KernelParameterMetadata
from agent_framework.openai import OpenAIResponsesClient


# ---- Define your data model ----
# The SK Azure AI Search connector can infer schema from annotated attributes.
# Keep it simple and flat to start.
class SupportArticle:
    article_id: str
    title: str
    content: str
    category: str


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}\n"
            f"Set it in your shell, e.g.:\n  export {name}='...'"
        )
    return value


async def main() -> None:
    # ---- Basic env validation (fail fast) ----
    _require_env("OPENAI_API_KEY")
    _require_env("AZURE_AI_SEARCH_ENDPOINT")
    _require_env("AZURE_AI_SEARCH_API_KEY")

    # ---- Create an Azure AI Search collection ----
    collection = AzureAISearchCollection[str, SupportArticle](
        record_type=SupportArticle,
        embedding_generator=OpenAITextEmbedding(),
    )

    async with collection:
        # Creates the backing index/collection if needed
        await collection.ensure_collection_exists()

        # ---- Create a search function from the collection ----
        search_function = collection.create_search_function(
            function_name="search_knowledge_base",
            description="Search the knowledge base for support articles and product information.",
            search_type="keyword_hybrid",
            parameters=[
                KernelParameterMetadata(
                    name="query",
                    description="The search query to find relevant information.",
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
            string_mapper=lambda x: f"[{x.record.category}] {x.record.title}: {x.record.content}",
        )

        # ---- Convert the search function to an Agent Framework tool ----
        search_tool = search_function.as_agent_framework_tool()

        # ---- Create an agent with the search tool ----
        agent = OpenAIResponsesClient(model_id="gpt-4o").as_agent(
            instructions=(
                "You are a helpful support specialist. "
                "Use the search tool to find relevant information before answering questions. "
                "Always cite your sources."
            ),
            tools=search_tool,
        )

        # ---- Use the agent with RAG capabilities ----
        response = await agent.run("How do I return a product?")
        print(response.text)


if __name__ == "__main__":
    asyncio.run(main())

"""
Notes / troubleshooting:

1) If ensure_collection_exists() fails complaining about missing collection/index name:
   The AzureAISearchCollection connector may require a collection/index name either via:
     - an argument in the constructor (varies by SK version), or
     - an environment variable (varies by SK version).
   In that case, check the connector docs/version you installed and set the required name.

2) If upsert() fails:
   Some SK versions expect a specific “record” wrapper type (not the plain model).
   Start by getting search working against an existing index, then adapt the upsert shape
   to your installed SK version.

3) Package versions move:
   The Microsoft migration guidance shows this exact pattern (create_search_function → as_agent_framework_tool → OpenAIResponsesClient.as_agent). :contentReference[oaicite:1]{index=1}
"""
