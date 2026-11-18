# Retrieval checklist

Each rule has a short rationale and the book section where the idea is explained.

## Choosing an approach

1. Context stuffing (placing the whole source in the prompt) fits small, stable sources that fit comfortably within the token budget, for example a few dozen pages. It avoids every retrieval failure at the cost of tokens per call. (Chapter 3, Context stuffing)
2. Cache-augmented generation (CAG) fits the same small, stable sources when calls are frequent: the source is loaded once into a cached prefix and reused, which cuts cost and latency. It requires a provider or runtime with prompt or KV caching. (Chapter 3, Cache-augmented generation)
3. RAG fits sources that are too large for the context window or the token budget, that change often, or whose parts need access control per user. (Chapter 3, Choosing an approach)
4. A hybrid fits mixed cases, for example a small stable core loaded into the context plus RAG over a large or changing archive. (Chapter 3, Choosing an approach)
5. State the assumption about size and change rate behind the recommendation, and when the recommendation would change. (Chapter 3, Choosing an approach)

## Ingestion and chunking

6. Chunks follow the structure of the documents (sections, paragraphs, list items, code blocks) and do not cut sentences or tables in half. Fixed-size character splitting without overlap breaks meaning at chunk boundaries. (Chapter 3, Chunking strategies)
7. Chunk size suits the questions asked: small enough for precise matches, large enough to carry the answer with its context. Some overlap between consecutive chunks keeps boundary information retrievable. (Chapter 3, Chunking strategies)
8. Each chunk carries metadata (source document, section, date, permissions) so retrieval can filter and answers can cite their source. (Chapter 3, The indexing pipeline)
9. The index is updated when the source changes, and stale chunks are removed. (Chapter 3, RAG in production environments)

## Retrieval and generation

10. The number of chunks placed in the prompt is small and justified. Passing dozens of chunks dilutes attention and raises cost. Retrieve more candidates and keep a few after reranking. (Chapter 3, The generation pipeline)
11. A reranking step, or a hybrid keyword plus vector search, is used when plain vector similarity returns near-duplicates or loosely related chunks. (Chapter 3, Retrieval models and vector databases)
12. Time-sensitive sources are filtered or weighted by date, so the model does not answer from outdated documents. (Chapter 3, RAG in production environments)
13. The prompt tells the model to answer from the retrieved context, to cite it, and to say when the context does not contain the answer. (Chapter 3, The generation pipeline)
14. Retrieval quality is measured with a small set of real questions and expected sources before and after each change. (Chapter 3, RAG in production environments)
