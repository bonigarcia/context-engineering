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

import re

from haystack import Document, Pipeline, component
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore


DOCUMENTS = [
    Document(content="Important notes stay pinned at the top of the workspace.", meta={"title": "Important notes"}),
    Document(content="Tagging groups related notes by project or topic.", meta={"title": "Tagging notes"}),
    Document(content="Archived notes remain searchable after the task is done.", meta={"title": "Archiving notes"}),
]


@component
class QueryAwareReranker:
    @component.output_types(documents=list[Document])
    def run(self, query: str, documents: list[Document]):
        tokens = set(re.findall(r"\w+", query.lower()))

        def rank(document: Document):
            title = str(document.meta.get("title", "")).lower()
            content = document.content.lower()
            title_boost = 2 if tokens & set(re.findall(r"\w+", title)) else 0
            content_overlap = len(tokens & set(re.findall(r"\w+", content)))
            return (title_boost, content_overlap, float(document.score or 0.0))

        return {"documents": sorted(documents, key=rank, reverse=True)}


def build_pipeline() -> Pipeline:
    document_store = InMemoryDocumentStore()
    document_store.write_documents(DOCUMENTS)

    pipeline = Pipeline()
    pipeline.add_component("retriever", InMemoryBM25Retriever(document_store=document_store))
    pipeline.add_component("reranker", QueryAwareReranker())
    pipeline.connect("retriever.documents", "reranker.documents")
    return pipeline


def run_query(query: str, top_k: int = 3) -> str:
    pipeline = build_pipeline()
    result = pipeline.run(
        {
            "retriever": {"query": query, "top_k": top_k},
            "reranker": {"query": query},
        }
    )
    documents = result["reranker"]["documents"]
    lines = ["Reranked results:"]
    for document in documents:
        lines.append(f"- {document.meta.get('title', 'Untitled')}: {document.content}")
    return "\n".join(lines)


if __name__ == "__main__":
    question = "Where do I find important notes?"
    print(f"Question: {question}")
    print(run_query(question))
