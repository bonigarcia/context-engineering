# Haystack

This Chapter 10 bucket shows Haystack as a local-first framework for assembling retrieval context in memory.

## Runnable examples

- `rag_pipeline/`: a minimal in-memory BM25 retrieval pipeline over a tiny LumaNote corpus.
- `reranking/`: a retrieval pipeline that reranks results with a lightweight query-aware scorer.
- `query_expansion/`: a pipeline that expands a query into a few local variants before retrieval.
- `pipeline_composition/`: a three-stage pipeline that composes retrieval, assembly, and formatting.
