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

from __future__ import annotations

from haystack import Document, Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore


DOCUMENTS = [
    Document(
        content="Use tags to group related notes and keep the workspace tidy.",
        meta={"title": "Organizing with tags"},
    ),
    Document(
        content="Pin a note to the top when it needs immediate attention.",
        meta={"title": "Pinning important notes"},
    ),
    Document(
        content="Archive finished notes instead of deleting them so they stay searchable.",
        meta={"title": "Archiving old notes"},
    ),
]


def build_pipeline() -> Pipeline:
    document_store = InMemoryDocumentStore()
    document_store.write_documents(DOCUMENTS)

    pipeline = Pipeline()
    pipeline.add_component("retriever", InMemoryBM25Retriever(document_store=document_store))
    return pipeline


def run_query(query: str, top_k: int = 2) -> str:
    pipeline = build_pipeline()
    result = pipeline.run({"retriever": {"query": query, "top_k": top_k}})
    documents = result["retriever"]["documents"]

    if not documents:
        return "No relevant notes found."

    lines = ["Retrieved context:"]
    for document in documents:
        title = document.meta.get("title", "Untitled")
        lines.append(f"- {title}: {document.content}")
    return "\n".join(lines)


if __name__ == "__main__":
    question = "How do I keep notes organized?"
    print(f"Question: {question}")
    print(run_query(question))
