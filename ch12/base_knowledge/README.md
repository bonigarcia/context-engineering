# Building a Base Knowledge Layer with Graphify

This hands-on example demonstrates how to build a persistent *Base Knowledge Layer* (vault) from technical literature, following the "LLM Knowledge Bases" pattern. Instead of feeding disconnected raw documents to an AI coding agent for every task, we extract structured entities, relationships, and communities to serve as a reliable, navigable context layer.

## Corpus of Literature

This example compiles structured knowledge extracted by the open-source tool Graphify(https://graphify.net/) from six papers reviewed in Chapter 12:

1. *Meta Context Engineering via Agentic Skill Evolution* (Ye et al., 2026)
2. *Context Engineering 2.0: The Context of Context Engineering* (Hua et al., 2025)
3. *LCM: Lossless Context Management* (Ehrlich et al., 2026)
4. *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models* (Zhang et al., 2025)
5. *Everything is Context: Agentic File System Abstraction for Context Engineering* (Xu et al., 2025)
6. *Multi-agent cooperation through in-context co-player inference* (Weis et al., 2026)

## Output Files (`graphify-out/`)

Graphify processes the raw literature to produce three primary outputs:

- `GRAPH_REPORT.md`: A summary text report identifying core abstractions ("God Nodes"), surprising cross-paper connections inferred by the model, semantic similarity edges, and detected knowledge gaps.
- `graph.json`: The raw graph serialization format containing the nodes (entities), edges (relationships), and community attributes used by downstream agents.
- `graph.html`: An interactive visual navigation graph that developers and agents can open in a browser to inspect entity clustering (e.g., *ACE Adaptation*, *Context Architecture*, *Lossless Memory*, *Filesystem Context*).

## Detected Communities

The graph separates the literature into 6 distinct semantic communities:
- Community 0 - "ACE Adaptation"* (ACE, Evolving Playbooks, Grow-and-Refine, Incremental Delta Updates)
- Community 1 - "Context Architecture" (Context Engineering 2.0, Context Isolation, Entropy Reduction, Layered Memory)
- Community 2 - "Skill Evolution" (Meta Context Engineering, Agentic Skill Evolution, Context as Files/Code)
- Community 3 - "Filesystem Context" (Everything is Context, Persistent Context Repository, File System Abstraction)
- Community 4 - "Lossless Memory" (LCM, Hierarchical Summary DAG, Operator-Level Recursion)
- Community 5 - "Multi-Agent Cooperation" (In-Context Co-Player Inference, Mixed-Pool Training)
