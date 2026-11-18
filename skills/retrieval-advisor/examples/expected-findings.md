# Expected findings

## examples/small-handbook

A correct review recommends context stuffing or cache-augmented generation (CAG) instead of RAG. The handbook is about 20,000 tokens, stable, readable by everyone, and queried often, so CAG is a strong choice and context stuffing is acceptable. It also reports that fixed 200-character chunks without overlap cut sentences and policies in half, and that chunks have no metadata (section, update date) for citation. It may note that recreating the collection on each run is fine for this size.

## examples/support-tickets

A correct review keeps RAG (`recommendation` is `rag`), since the archive is large and changes daily. It reports at least that:

- passing 50 tickets (`limit=50`) to the prompt is too many: retrieve candidates, rerank, and keep a few;
- there is no reranking step;
- retrieval ignores the ticket date and product version, although old resolutions are often wrong. Filter or weight by date and version.

It may also mention that the prompt does not ask the model to cite tickets or to say when no ticket applies.
