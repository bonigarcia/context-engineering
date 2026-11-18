"""Index the employee handbook for the HR assistant."""

from pathlib import Path

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

CHUNK_SIZE = 200  # characters

client = OpenAI()
store = QdrantClient(path="qdrant-data")


def chunk(text):
    return [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]


def main():
    text = Path("handbook.md").read_text(encoding="utf-8")
    chunks = chunk(text)
    store.recreate_collection("handbook", vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
    vectors = client.embeddings.create(model="text-embedding-3-small", input=chunks).data
    points = [PointStruct(id=i, vector=v.embedding, payload={"text": c}) for i, (c, v) in enumerate(zip(chunks, vectors))]
    store.upsert("handbook", points)


if __name__ == "__main__":
    main()
