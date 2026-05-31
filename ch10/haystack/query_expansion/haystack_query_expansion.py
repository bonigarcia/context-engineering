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

from collections import OrderedDict

from haystack import Document, Pipeline, component
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore


DOCUMENTS = [
    Document(content="Sync notes from every device after you sign in.", meta={"title": "Syncing notes"}),
    Document(content="Backup notes regularly so you can restore them later.", meta={"title": "Backing up notes"}),
    Document(content="Organize notes with tags and folders.", meta={"title": "Organizing notes"}),
]


@component
class QueryExpander:
    @component.output_types(queries=list[str])
    def run(self, query: str):
        variants = [query.strip()]
        normalized = query.lower().strip()
        if "sync" in normalized:
            variants.append(normalized.replace("sync", "backup"))
            variants.append(normalized.replace("sync", "synchronize"))
        if "organize" in normalized:
            variants.append(normalized.replace("organize", "tag"))
        return {"queries": list(dict.fromkeys(variants))}


@component
class ExpandedRetriever:
    def __init__(self):
        self.document_store = InMemoryDocumentStore()
        self.document_store.write_documents(DOCUMENTS)
        self.retriever = InMemoryBM25Retriever(document_store=self.document_store)

    @component.output_types(documents=list[Document])
    def run(self, queries: list[str], top_k: int = 2):
        merged: OrderedDict[str, Document] = OrderedDict()
        for query in queries:
            for document in self.retriever.run(query=query, top_k=top_k)["documents"]:
                key = document.meta.get("title", document.content)
                if key not in merged:
                    merged[key] = document
        return {"documents": list(merged.values())}


def build_pipeline() -> Pipeline:
    pipeline = Pipeline()
    pipeline.add_component("expander", QueryExpander())
    pipeline.add_component("collector", ExpandedRetriever())
    pipeline.connect("expander.queries", "collector.queries")
    return pipeline


def run_query(query: str, top_k: int = 2) -> str:
    pipeline = build_pipeline()
    result = pipeline.run({"expander": {"query": query}, "collector": {"top_k": top_k}})
    documents = result["collector"]["documents"]
    lines = ["Expanded retrieval:"]
    for document in documents:
        lines.append(f"- {document.meta.get('title', 'Untitled')}: {document.content}")
    return "\n".join(lines)


if __name__ == "__main__":
    question = "sync notes"
    print(f"Question: {question}")
    print(run_query(question))
