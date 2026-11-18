"""Retrieve similar resolved tickets for the support copilot."""

from openai import OpenAI
from qdrant_client import QdrantClient

client = OpenAI()
store = QdrantClient(url="http://localhost:6333")


def similar_tickets(question):
    vector = client.embeddings.create(model="text-embedding-3-small", input=[question]).data[0].embedding
    hits = store.search(collection_name="tickets", query_vector=vector, limit=50)
    return [hit.payload["text"] for hit in hits]


def build_prompt(question):
    context = "\n\n".join(similar_tickets(question))
    return f"Resolved tickets:\n{context}\n\nNew ticket:\n{question}\n\nSuggest a reply."
