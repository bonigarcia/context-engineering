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

from haystack import Document, Pipeline, component
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore


DOCUMENTS = [
    Document(content="Haystack pipelines keep retrieval, assembly, and formatting separate when you organize notes.", meta={"title": "Pipeline composition"}),
    Document(content="A small pipeline is easier to test when each component does one job.", meta={"title": "Single-purpose stages"}),
    Document(content="Local pipelines can still combine multiple steps without external services.", meta={"title": "Local composition"}),
]


@component
class ContextAssembler:
    @component.output_types(context=str)
    def run(self, documents: list[Document]):
        lines = []
        for document in documents:
            lines.append(f"{document.meta.get('title', 'Untitled')}: {document.content}")
        return {"context": "\n".join(lines)}


@component
class ResponseFormatter:
    @component.output_types(answer=str)
    def run(self, context: str):
        return {
            "answer": (
                "Pipeline composition answer:\n"
                "- retrieval gathers the local notes\n"
                "- assembly turns them into a readable context\n"
                f"- final context:\n{context}"
            )
        }


def build_pipeline() -> Pipeline:
    document_store = InMemoryDocumentStore()
    document_store.write_documents(DOCUMENTS)

    pipeline = Pipeline()
    pipeline.add_component("retriever", InMemoryBM25Retriever(document_store=document_store))
    pipeline.add_component("assembler", ContextAssembler())
    pipeline.add_component("formatter", ResponseFormatter())
    pipeline.connect("retriever.documents", "assembler.documents")
    pipeline.connect("assembler.context", "formatter.context")
    return pipeline


def run_query(query: str, top_k: int = 2) -> str:
    pipeline = build_pipeline()
    result = pipeline.run({"retriever": {"query": query, "top_k": top_k}})
    return result["formatter"]["answer"]


if __name__ == "__main__":
    question = "organize notes"
    print(f"Question: {question}")
    print(run_query(question))
