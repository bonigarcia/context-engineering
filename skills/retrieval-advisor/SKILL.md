---
name: retrieval-advisor
description: "Reviews how an LLM application brings external knowledge into the context: a RAG pipeline (ingestion, chunking, embeddings, retrieval, reranking) or a plan for one. Recommends RAG, cache-augmented generation (CAG), context stuffing, or a hybrid for the given corpus, and reports pipeline problems. Use when the user asks whether they need RAG, or asks to review or improve retrieval, chunking, or a knowledge base integration. Do not use for agent memory design (use memory-designer) or for general prompt review."
license: Apache-2.0
metadata:
  chapter: "3"
  chapter-title: "External knowledge and retrieval"
  input: "A RAG pipeline (code and configuration) or a description of a knowledge source"
  output: "Recommendation among RAG, CAG, and context stuffing, plus pipeline findings"
---

# Retrieval advisor

Decide how this system should bring external knowledge into the model's context, and point out what in the current pipeline hurts answer quality or cost.

## Procedure

1. Identify the knowledge source: its size (pages, documents, or tokens), how often it changes, its structure, and who can see which parts. If the user did not say, infer it from the code or data and state your assumption.
2. Identify the current approach, if any: how documents are loaded, split, embedded, stored, retrieved, filtered, reranked, and placed in the prompt.
3. Read `references/checklist.md`. Use its decision rules to choose a recommendation, and check the pipeline against its review rules.
4. Write the report described below, with a `## Recommendation` section after the findings that explains the choice in a few sentences, including when the recommendation would change.

## Report format

Write the report in Markdown, in this order:

1. `## Summary`: two to four sentences on the overall state and the most important change.
2. `## Findings`: one bullet per finding, most severe first, in the form `- [severity] location: problem. Fix: suggested fix. (book section)`. Severity is `high` when the problem causes wrong or unsafe behavior, `medium` when it makes results unreliable or costly, and `low` for clarity or maintenance issues. If there are no problems, write `No findings.`
3. Any skill-specific section named in the procedure.
4. A final fenced `json` block with the same content, as in this example. Set `recommendation` to one of these values. `rag`: retrieve chunks per query. `cag`: load the whole source once into a cached prefix. `context-stuffing`: place the whole source in every prompt. `hybrid`: part of the source in the context and RAG for the rest. Hybrid keyword and vector search is still `rag`.

```json
{
  "skill": "retrieval-advisor",
  "summary": "...",
  "recommendation": "rag",
  "findings": [
    {
      "severity": "high",
      "location": "ingest.py, chunking",
      "problem": "...",
      "fix": "...",
      "book_section": "Chapter 3, Chunking strategies"
    }
  ]
}
```

Use the book section given in the checklist for each rule. If the input is missing or out of scope for this skill, say so in one sentence and stop.

Learn more: Chapter 3 of *Context Engineering* (Manning), https://hubs.la/Q04ksQ8J0
