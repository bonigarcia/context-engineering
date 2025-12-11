# Context engineering

**Context engineering** can be defined as the practice of designing systems that provide a Large Language Model (LLM) with all the necessary information to complete a task effectively. It goes beyond prompt engineering since it focuses on building a comprehensive and structured context from various sources like system instructions, external knowledge, memory, tools, and state. The central idea is that the success of a complex LLM-based system depends more on the quality and completeness of the context provided than on the specific wording of the prompt itself.

Tobi Lütke, the CEO of Shopify, coined the term _context engineering_ in a [tweet](https://x.com/tobi/status/1935533422589399127) on June 19, 2025. He defined context engineering as _the art of providing all the context for the task to be plausibly solvable by the LLM_. This novel concept captures the essence of the current evolution of LLM-based systems, inspiring others (like me) to understand and define this emerging engineering discipline. Since then, I've been working on a book entitled **Context engineering: the art and science of shaping context-aware AI systems**, to be published by [Manning](https://www.manning.com/) in 2026.

This GitHub repository is intended to be a companion resource for this book and a go-to reference for practitioners looking to understand and adopt the context engineering principles.

_Warning_: This repository is a work in progress, so content and structure may change.

## Table of contents

This book aims to provide a strong, general-purpose theoretical foundation for context engineering, supported by hands-on examples. Its table of contents is the following:

1. Introduction to context engineering
2. System instructions and user prompts
3. Retrieval and external knowledge
4. Tools and memory for AI agents
5. State and multi-agent systems
6. Context management and evaluation
7. Context in AI frameworks
8. Context engineering in real-world environments
9. Context engineering through the software development lifecycle
10. State of the art on context engineering  
Appendix A. The AI ecosystem

Each chapter of this book starts by explaining the underlying principles and patterns of each thematic block. Then, the final part of each chapter is devoted to presenting specific examples. This GitHub repository contains all these examples. Moreover, I will include new examples and maintain the existing ones even after the book is published. The goal is to provide an open-source, updated reference for everyone interested in context engineering.

## Online tool

This repo also hosts the [context-aware prompt builder](https://bonigarcia.dev/context-engineering/context-aware-prompt-builder.html), an online tool presented in chapter 2 for designing, comparing, and reusing structured prompts across multiple frameworks and AI models.

## Resources
Although the concept of _context engineering_ is new, the underlying technologies (LLMs, AI agents, prompt engineering, RAG, MCP, memory management, etc.) have been developed over the years. Nevertheless, summarizing all these converging technologies and tools in a single book is a very challenging task. As you know, nowadays there is more information than ever, and it is very easy to get lost with so many sources. This section summarizes some of the most relevant references and resources I found during my journey to unravel the essence of context engineering.


### Context Engineering

- [The rise of "context engineering"](https://blog.langchain.com/the-rise-of-context-engineering/) (LangChain, Jun 23, 2025) Overview of context engineering as an emerging essential skill for AI engineers building dynamic, tool-using systems.
- [Context Engineering](https://blog.langchain.com/context-engineering-for-agents/) (LangChain, Jul 02, 2025) Breakdown of strategies (write, select, compress, isolate) for filling an agent's context window with only the most relevant information at each step.
- [From Vibe Coding to Context Engineering: A Blueprint for Production-Grade GenAI Systems](https://www.sundeepteki.org/blog/from-vibe-coding-to-context-engineering-a-blueprint-for-production-grade-genai-systems) (Sundeep Teki, Jul 07, 2025) Ad-hoc vibe coding doesn't scale and proposing context engineering as a disciplined approach for production-grade GenAI systems.
- [What is Context Engineering: Clearly Explained](https://apidog.com/blog/context-engineering/) (Ashley Goolam, Jul 09, 2025) Introduction of context components (instructions, history, tools, external data) and why high-quality context is often more important than model size.
- [Context Engineering: Bringing Engineering Discipline to Prompts](https://addyo.substack.com/p/context-engineering-bringing-engineering) (Addy Osmani, Jul 13, 2025) Explanation of context engineering as providing models with structured, complete context-beyond prompt tweaking to increase reliability.
- [The AI Skeptic's Guide to Context Windows](https://block.github.io/goose/blog/2025/08/18/understanding-context-windows/) (Rizel Scarlett, Aug 18, 2025) Critical look at the limitations of LLM context windows and how context engineering mitigates overload, noise, and degradation.
- [Context Engineering - Making Every Token Count](https://speakerdeck.com/addyosmani/context-engineering-making-every-token-count) (Addy Osmani, Sep 09, 2025) Talk about how to structure and manage context for AI systems to produce better, more reliable outputs.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (Anthropic, Sep 29, 2025) Introduction about context engineering, i.e., carefully curating and limiting what information an AI agent sees.
- [Context Engineering Guide](https://www.promptingguide.ai/guides/context-engineering-guide) (PromptingGuide.ai, 2025) Guide defining context engineering as architecting and optimizing all information fed into an LLM to improve output quality and reduce errors.
- [Context Engineering – Short-Term Memory Management with Sessions from OpenAI Agents SDK](https://cookbook.openai.com/examples/agents_sdk/session_memory) (OpenAI, 2025) Practical demonstration of managing short-term memory using sessions, showing how structured context improves coherence in multi-step agent interactions.
- [Context Engineering: Sessions, Memory](https://www.kaggle.com/whitepaper-context-engineering-sessions-and-memory) (Kimberly Milam et al., 2025) Whitepaper describing how to engineer session and long-term memory to support reliable, stateful AI agents.
- [The Context Engineering Guide](https://weaviate.io/ebooks/the-context-engineering-guide) (Weaviate, 2025) Guide explaining how to design, structure, and optimize context for LLM applications, including chunking, retrieval, memory, and agent workflows.


### Prompt Engineering

- [Prompt Engineering](https://www.kaggle.com/whitepaper-prompt-engineering) (Lee Boonstra, 2025) Overview of prompt engineering principles and methods aimed at helping developers construct effective prompts for LLMs.
- [Prompt Engineering Guide](https://www.promptingguide.ai/) (PromptingGuide.ai, 2025) Guide that defines prompt engineering as a discipline for designing and optimizing prompts to make LLMs perform better on diverse tasks, offering techniques, references, and best practices.
- [The Prompt Engineering Playbook for Programmers](https://addyo.substack.com/p/the-prompt-engineering-playbook-for) (Addy Osmani, 2025) Practical playbook targeting programmers, giving structured guidelines and patterns for writing prompts that yield consistent and reliable outputs from AI.
- [Anthropic's Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) (Anthropic, 2025) Hands-on tutorial that walks users step-by-step through designing and refining prompts (with exercises and example-based practice) to get better results from their models.
- [Meta's prompt engineering guide](https://llama.meta.com/docs/how-to-guides/prompting/) (Meta, 2025) Guide describing how to craft prompts for their models, covering best practices to structure instructions, context, and examples for improved performance.
- [Google's Gemini prompt engineering guide](https://services.google.com/fh/files/misc/gemini-for-google-workspace-prompting-guide-101.pdf) (Google, 2025) How to write effective prompts for Google's Gemini (or related models), emphasizing clarity, context, and structured prompting for reliable responses.
- [Prompt examples, by OpenAI](https://platform.openai.com/examples) (OpenAI, 2025) Collection of sample prompts illustrating good practices and giving real-world examples to help users understand how to frame prompts effectively for best results.
- [Prompt Library, by Anthropic](https://docs.anthropic.com/en/prompt-library/library) (Anthropic, 2025) Repository of tested prompt templates and examples, serving as a practical library for users to build on and adapt for their own AI tasks.


### AI Agents

- [Introduction to Agents, by Alan Blount et al.](https://www.kaggle.com/whitepaper-introduction-to-agents) (Alan Blount et al., 2025) Definition of agent as a complete application, combining LLM reasoning, tooling and orchestration that plans and acts autonomously rather than just responding to single prompts.
- [What are AI Agents? Why do they matter?](https://addyo.substack.com/p/what-are-ai-agents-why-do-they-matter) (Addy Osmani, 2025) Explanation that AI agents are programs that use language models and tools to perform goal-driven tasks, emphasizing their importance for automating complex workflows.
- [Agents Companion, by Antonio Gulli et al.](https://www.kaggle.com/whitepaper-agent-companion) (Antonio Gulli et al., 2025) Whitepaper presenting production-grade considerations for agents: orchestration, memory, evaluation, multi-agent coordination and deployment best practices.
- [The AI agents stack](https://www.letta.com/blog/ai-agents-stack) (Letta, 2025) Overview of the technological layers and components (models, tools, orchestration, memory, environment interfaces) that constitute a full-fledged AI-agents infrastructure.
- [Gemini CLI Tips & Tricks](https://addyo.substack.com/p/gemini-cli-tips-and-tricks) (Addy Osmani, 2025) Practical advice and examples on using the Gemini CLI tool effectively when building or interacting with AI agents.
- [Memory by LangGraph](https://langchain-ai.github.io/langgraph/concepts/memory/) (LangGraph, 2025) Guide about memory management techniques and how to maintain agent state across interactions to support coherent, long-lived agent sessions.
- [Gemini with memory](https://www.philschmid.de/gemini-with-memory) (Phil Schmid, 2025) Tutorial showing how to integrate persistent memory mechanisms into agents using Gemini, enabling context-aware, multi-step workflows.
- [Agent Quality](https://www.kaggle.com/whitepaper-agent-quality) (Meltem Subasioglu et al., 2025) Research-oriented paper evaluating metrics and benchmarks for assessing agent performance, robustness and reliability across tasks.
- [Open Source LLM Tools](https://huyenchip.com/llama-police) (Huyenchip, 2025) Curated list and analysis of open-source tools for building, evaluating or deploying LLM-based agents.
- [The AI agents stack](https://www.letta.com/blog/ai-agents-stack) (Letta, 2025) Article outlining the architecture layers (model, tools, memory, orchestration) that build up modern AI-agent systems.
- [AG-UI: Agents to users](https://github.com/ag-ui-protocol/ag-ui) (AG-UI community, 2025) Open-source project aiming to provide user-facing UI/UX for agent-based systems.
- [Awesome Neuron](https://awesomeneuron.substack.com/) (Awesome Neuron, 2025) Newsletter/blog exploring recent developments, tools and ideas around neural-agent frameworks and agentic AI.


### MCP

- [Model Context Protocol](https://modelcontextprotocol.io/) (Anthropic, Nov 25, 2024) Open-source standard for connecting LLMs and AI agents to external data sources, tools and services.
- [Agent Tools & Interoperability with MCP](https://www.kaggle.com/whitepaper-agent-tools-and-interoperability-with-mcp) (Mike Styer et al., 2025) Analysis of how using MCP enables consistent interoperability between AI agents and external tools/services.
- [MCP: What It Is and Why It Matters](https://addyo.substack.com/p/mcp-what-it-is-and-why-it-matters) (Addy Osmani, 2025) Overview of MCP's purpose: to standardize how AI applications access external tools/data.
- [Function calling & MCP for LLMs](https://blog.dailydoseofds.com/p/function-calling-and-mcp-for-llms) (Avi Chawla, Apr 19, 2025) Explains how MCP builds on earlier function-calling approaches by standardizing how LLMs invoke external tools and data sources.
- [Find Awesome MCP Servers and Clients](https://mcp.so/) (Community, 2025) Curated directory of publicly available MCP servers and client libraries, helping developers locate ready-made integrations to connect models to data sources or tools.
- [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers) (Anthropic, 2025) Repository of reference implementations of MCP servers, providing working examples to help developers deploy MCP-compatible services.
- [The Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions](https://arxiv.org/abs/2503.23278) (Xinyi Hou et al., Mar 30, 2025) Academic analysis of MCP's architecture, use cases, and ecosystem, including a survey of adoption, security/privacy risks, and recommendations for safe, sustainable development.
- [Model Context Protocol at First Glance: Studying the Security and Maintainability of MCP Servers](https://arxiv.org/abs/2506.13538) (Mohammed Mehedi Hasan et al., Jun 16, 2025) Empirical study showing that while many open-source MCP servers are healthy and maintained, a non-trivial fraction have security vulnerabilities or tool-poisoning risks.


### Retrieval and RAG

- [Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/information-retrieval-book.html) (Christopher Manning et al., 2008) Classic textbook covering foundational concepts in information retrieval, indexing, search algorithms, ranking, etc.
- [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) (Anthropic, Sep 19, 2024) Introduction of Contextual Retrieval, a method that enriches document chunks with additional context before embedding/indexing to improve accuracy and reduce context loss in RAG systems.
- [Chunking Strategies for LLM Applications, by Pinecone](https://www.pinecone.io/learn/chunking-strategies/) (Pinecone, 2025) Guide explaining how to break large texts into appropriately sized chunks before embedding, a critical step for effective retrieval and generation with LLM-based applications.
- [Retrieval, by LangChain](https://docs.langchain.com/oss/javascript/langchain/retrieval) (LangChain, 2025) Reference documentation on retrieval functionality in LangChain, describing how to integrate vector-based retrieval into LLM workflows.
- [What is Agentic RAG](https://weaviate.io/blog/what-is-agentic-rag) (Weaviate, 2025) Explanation of “Agentic RAG,” a paradigm that combines retrieval-augmented generation with autonomous agents, enabling multi-step reasoning, tool use, and dynamic retrieval for complex workflows.
- [Thinking Beyond RAG: Why Context-Augmented Generation Is Changing the Game](https://www.helicone.ai/blog/implement-and-monitor-cag) (Yusuf Ishola, 2025) Explanation of Context-Augmented Generation and how it improves over traditional RAG.
- [RAG vs CAG vs Fine-Tuning](https://newsletter.rafapaez.com/p/rag-vs-cag-vs-fine-tuning) (Rafa Paez, 2025) Comparative analysis of three approaches: Retrieval-Augmented Generation (RAG), Contextual Augmented Generation (CAG), and fine-tuning, discussing trade-offs in accuracy, adaptability, cost, and maintenance for each.


### AI for software development

- [The AI-Native Software Engineer](https://substack.com/home/post/p-165160941) (Addy Osmani, Jul 01, 2025) Essay exploring what it means to be a software engineer in a world where AI is deeply integrated, focusing on new skills, responsibilities, and the evolving identity of engineers.
- [The reality of AI-Assisted software engineering productivity](https://addyo.substack.com/p/the-reality-of-ai-assisted-software) (Addy Osmani, Aug 16, 2025) Recent evidence showing that AI can accelerate parts of coding but often leaves the last 30%: debugging, maintenance, and architectural decisions, to humans, arguing the future is human and AI, not AI-alone.
- [Vibe coding is not the same as AI-Assisted engineering](https://addyo.substack.com/p/vibe-coding-is-not-the-same-as-ai) (Addy Osmani, Aug 30, 2025) Warns against conflating vibe coding (prompt-driven quick prototyping) with robust, production-ready AI-assisted engineering, highlighting differences in ownership, quality, and maintainability.
- [Coding for the Future Agentic World](https://addyo.substack.com/p/coding-for-the-future-agentic-world) (Addy Osmani, 2025) Overview of how developers should adapt their workflows and mindset to build for an agentic world, where AI agents are first-class collaborators in software development.
- [Conductors to Orchestrators: The Future of Agentic Coding](https://addyo.substack.com/p/conductors-to-orchestrators-the-future) (Addy Osmani, Nov 01, 2025) Software engineers will shift from writing code (coder) to directing AI agents (conductor) and ultimately to overseeing fleets of agents (orchestrator), redefining the role of developers in the agent-driven future.


### Other similar books

- [AI Engineering: building applications with foundation models](https://www.oreilly.com/library/view/ai-engineering/9781098166298) (Chip Huyen, Dec 04, 2024) Overview of how to build real-world applications using foundation models covering model selection, evaluation, prompt engineering, RAG, agents, deployment, and best practices for reliability and scalability.
- [AI Agents in Action](https://www.manning.com/books/ai-agents-in-action) (Micheal Lanham, 2025) Practical guide to designing, building and deploying LLM-powered autonomous agents and multi-agent systems, including memory, tool integration, orchestration, and real-world use cases.
- [Building AI Agents with LLMs, RAG, and Knowledge Graphs](https://www.packtpub.com/en-us/product/building-ai-agents-with-llms-rag-and-knowledge-graphs-9781835080382) (Salvatore Raieli & Gabriele Iuculano, Jul 2025) Step-by-step book showing how to combine LLMs with RAG and knowledge graphs to build agents capable of grounded reasoning, tool use, planning and complex task execution.
- [AI Agents: The Definitive Guide](https://learning.oreilly.com/library/view/ai-agents-the/0642572247775/) (Nicole Koenigstein, 2025) Designing, evaluating, and deploying AI agents; covers architecture, memory, tools, orchestration and production-grade considerations.
- [Context Engineering for Multi-Agent Systems](https://www.packtpub.com/en-us/product/context-engineering-for-multi-agent-systems-9781806690046) (Denis Rothman, 2025) Design, manage and optimize context flow and memory across multi-agent systems to ensure coherent, efficient, and scalable interactions.
- [An Illustrated Guide to AI Agents](https://learning.oreilly.com/library/view/an-illustrated-guide/9798341662681/) (Maarten Grootendorst, Jay Alammar, 2025) Conceptual guide that explains agents, memory, tool use, workflows for agent-based AI.
- [Generative AI for Software Development](https://learning.oreilly.com/library/view/generative-ai-for/9781098162269/) (Sergio Pereira, 2025) Generative AI and LLMs leveraged to assist software development, including coding, documentation, and planning, via agentic or semi-agentic patterns.
- [Beyond Vibe Coding: A practical guide to AI-assisted development](https://beyond.addy.ie/) (Addy Osmani, 2025) Practical handbook advocating for structured, engineering-style workflows (not ad-hoc prompts) when using AI in software development, emphasizing reproducibility, context management, and scalable patterns.

### Other similar GitHub repositories

- [AI Engineering](https://github.com/chiphuyen/aie-book/) (Chip Huyen, 2025) AI engineering principles, covering data pipelines, LLM systems, deployment, evaluation, and production readiness.
- [AI Engineering Toolkit](https://github.com/Sumanth077/ai-engineering-toolkit) (Sumanth077, 2025) Collection of tools, templates, and best practices to support building, testing, and deploying AI/LLM-powered applications.
- [Agents Towards Production](https://github.com/NirDiamant/agents-towards-production) (Nir Diamant, 2025) Practical resources and examples demonstrating how to take AI agents from experimentation to reliable production systems.
- [Awesome generative AI guide](https://github.com/aishwaryanr/awesome-generative-ai-guide) (Aishwaryanr, 2025) Curated set of learning resources, papers, tools, and tutorials for understanding and applying generative AI.
- [Awesome LLM Apps](https://github.com/Shubhamsaboo/awesome-llm-apps) (Shubham Saboo, 2025) Curated list of real-world LLM application examples demonstrating practical use cases and design patterns.
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) (punkpeye, 2025) Directory of MCP servers, tools, and integrations to help developers adopt the MCP ecosystem.
- [Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering) (Meirtz, 2025) Curated list of papers, tools, articles, and examples focused on context engineering for LLMs and agents.
- [Best AI and LLM Engineering Resources](https://github.com/javabuddy/best-ai-and-llm-engineering-resource) (Javin Paul, 2025) Large curated repository of high-quality resources on AI engineering, LLM workflows, prompt design, and system patterns.
- [Brex's prompt engineering guide](https://github.com/brexhq/prompt-engineering) (Brex, 2025) Practical prompt engineering guide from Brex, including patterns, examples, and structured instructions for improving LLM output quality.
- [Context Engineering](https://github.com/davidkimai/Context-Engineering) (David Kim, 2025) Open resource explaining the concepts, patterns, and techniques of context engineering for AI systems.
- [Context Engineering Template](https://github.com/coleam00/context-engineering-intro) (Cole Medin, 2025) Starter template that introduces context engineering concepts and provides structure for building context-optimized LLM applications.
- [Context Engineering for Multi-Agent Systems](https://github.com/Denis2054/Context-Engineering-for-Multi-Agent-Systems) (Denis Rothman, 2025) Repository exploring how to design and manage context flows within multi-agent architectures.
- [Generative AI for beginners](https://github.com/microsoft/generative-ai-for-beginners) (Microsoft, 2025) Beginner-friendly curriculum teaching the fundamentals of generative AI, including notebooks, examples, and guided lessons.
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) (DAIR.AI, 2025) Extensive guide covering prompt engineering techniques, examples, patterns, and best practices for working with LLMs.
- [RAG-Anything: All-in-One RAG Framework](https://github.com/HKUDS/RAG-Anything) (Data Intelligence Lab@HKU, 2025) Open-source framework providing an all-in-one pipeline for RAG.
- [Top GitHub Context Engineering repositories](https://github.com/topics/context-engineering) (GitHub, 2025) Automatically aggregated GitHub topics of public repositories related to "context engineering."


### Papers

- Mei, Lingrui, Jiayu Yao, Yuyao Ge, Yiwei Wang, Baolong Bi, Yujun Cai, Jiazhi Liu et al. "[A Survey of Context Engineering for Large Language Models](https://arxiv.org/abs/2507.13334)." arXiv preprint arXiv:2507.13334 (2025).
- Hua, Qishuo, Lyumanshan Ye, Dayuan Fu, Yang Xiao, Xiaojie Cai, Yunze Wu, Jifan Lin, Junfei Wang, and Pengfei Liu. "[Context Engineering 2.0: The Context of Context Engineering](https://arxiv.org/abs/2510.26493)." arXiv preprint arXiv:2510.26493 (2025).
- Zhang, Qizheng, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton et al. "[Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618)." arXiv preprint arXiv:2510.04618 (2025).


## Contributing

Any comments or feedback are more than welcome. Also, if you think something can be improved or want to contribute to this repo, please open a [pull request](https://github.com/bonigarcia/context-engineering/pulls).

## About

context-engineering (Copyright &copy; 2025) is an open-source project created and maintained by [Boni Garcia](https://bonigarcia.dev/), licensed under the terms of [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).