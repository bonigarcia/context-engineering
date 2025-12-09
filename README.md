# Context engineering

**Context engineering** is an emerging term in AI, and it can be defined as the practice of designing systems that provide a Large Language Model (LLM) with all the necessary information to complete a task effectively. It goes beyond prompt engineering since it focuses on building a comprehensive and structured context from various sources like system instructions, external knowledge, memory, tools, and state. The central idea is that the success of a complex LLM-based system depends more on the quality and completeness of the context provided than on the specific wording of the prompt itself.

Tobi Lütke, the CEO of Shopify, coined the term _context engineering_ in a [tweet](https://x.com/tobi/status/1935533422589399127) on June 19, 2025. He defined context engineering as _the art of providing all the context for the task to be plausibly solvable by the LLM_. This novel concept captures the essence of the current evolution of LLM-based systems, inspiring others (like me) to understand and define this emerging engineering discipline. Since then, I've been working on a book entitled **Context engineering: the art and science of shaping context-aware AI systems**, to be published by [Manning](https://www.manning.com/) in 2026.

This GitHub repository is intended to be a companion resource for this book and a go-to reference for practitioners looking to understand and adopt the context engineering principles.

_Warning_: This repository is a work in progress — content and structure may change.

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

Although the concept of _context engineering_ is new, the underlying technologies (LLMs, AI agents, prompt engineering, RAG, MCP, memory management, etc.) have been developed over the years. Nevertheless, summarizing all these converging technologies and tools in a single book is a very challenging task. As you know, nowadays there is more information than ever, and it is very easy to get lost with so many sources. The only solution I found for this problem is to select the best references I could find, read and understand them, and put them into practice with ready-to-execute practical examples. This section summarizes some of the most relevant references and sources I found during my journey to unravel the essence of context engineering.

### Context Engineering

- [Context Engineering: Sessions & Memory](https://www.kaggle.com/whitepaper-context-engineering-sessions-and-memory)
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context Engineering - Making Every Token Count](https://speakerdeck.com/addyosmani/context-engineering-making-every-token-count)
- [From Vibe Coding to Context Engineering: A Blueprint for Production-Grade GenAI Systems](https://www.sundeepteki.org/blog/from-vibe-coding-to-context-engineering-a-blueprint-for-production-grade-genai-systems)
- [Context Engineering: Bringing Engineering Discipline to Prompts](https://addyo.substack.com/p/context-engineering-bringing-engineering)
- [Context Engineering Guide](https://www.promptingguide.ai/guides/context-engineering-guide)
- [The rise of "context engineering"](https://blog.langchain.com/the-rise-of-context-engineering/)
- [Context Engineering (by LangChain)](https://blog.langchain.com/context-engineering-for-agents/)
- [What is Context Engineering: Clearly Explained](https://apidog.com/blog/context-engineering/)
- [The AI Skeptic's Guide to Context Windows](https://block.github.io/goose/blog/2025/08/18/understanding-context-windows/)
- [Context Engineering - Short-Term Memory Management with Sessions from OpenAI Agents SDK](https://cookbook.openai.com/examples/agents_sdk/session_memory)

### Prompt Engineering

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Prompt Engineering (by Lee Boonstra)](https://www.kaggle.com/whitepaper-prompt-engineering)
- [The Prompt Engineering Playbook for Programmers](https://addyo.substack.com/p/the-prompt-engineering-playbook-for)
- [Anthropic's Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
- [Meta's prompt engineering guide](https://llama.meta.com/docs/how-to-guides/prompting/)
- [Google's Gemini prompt engineering guide](https://services.google.com/fh/files/misc/gemini-for-google-workspace-prompting-guide-101.pdf)
- [Prompt examples, by OpenAI](https://platform.openai.com/examples)
- [Prompt Library, by Anthropic](https://docs.anthropic.com/en/prompt-library/library)


### AI Agents

- [Introduction to Agents](https://www.kaggle.com/whitepaper-introduction-to-agents)
- [Agents Companion](https://www.kaggle.com/whitepaper-agent-companion)
- [What are AI Agents? Why do they matter?](https://addyo.substack.com/p/what-are-ai-agents-why-do-they-matter)
- [AG-UI: Agents to users](https://github.com/ag-ui-protocol/ag-ui)
- [The AI agents stack](https://www.letta.com/blog/ai-agents-stack)
- [Awesome Neuron](https://awesomeneuron.substack.com/)
- [Open Source LLM Tools](https://huyenchip.com/llama-police)
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)
- [Gemini CLI Tips & Tricks](https://addyo.substack.com/p/gemini-cli-tips-and-tricks)
- [Memory by LangGraph](https://langchain-ai.github.io/langgraph/concepts/memory/)
- [Gemini with memory](https://www.philschmid.de/gemini-with-memory)


### MCP

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent Tools & Interoperability with MCP](https://www.kaggle.com/whitepaper-agent-tools-and-interoperability-with-mcp)
- [MCP: What It Is and Why It Matters](https://addyo.substack.com/p/mcp-what-it-is-and-why-it-matters)
- [Function calling & MCP for LLMs](https://blog.dailydoseofds.com/p/function-calling-and-mcp-for-llms)
- [Find Awesome MCP Servers and Clients](https://mcp.so/)
- [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers)

### Retrieval RAG

- [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [Chunking Strategies for LLM Applications, by Pinecone](https://www.pinecone.io/learn/chunking-strategies/)
- [Retrieval, by LangChain](https://docs.langchain.com/oss/javascript/langchain/retrieval)
- [Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/information-retrieval-book.html)
- [What is Agentic RAG](https://weaviate.io/blog/what-is-agentic-rag)
- [RAG vs CAG vs Fine-Tuning](https://newsletter.rafapaez.com/p/rag-vs-cag-vs-fine-tuning)


### Books

- [AI Engineering: building applications with foundation models](https://www.oreilly.com/library/view/ai-engineering/9781098166298)
- [AI Agents in Action](https://www.manning.com/books/ai-agents-in-action)
- [Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems](https://link.springer.com/book/10.1007/978-3-032-01402-3)
- [Building AI Agents with LLMs, RAG, and Knowledge Graphs](https://www.packtpub.com/en-us/product/building-ai-agents-with-llms-rag-and-knowledge-graphs-9781835080382)
- [Beyond Vibe Coding: A practical guide to AI-assisted development](https://beyond.addy.ie/)
- [The Agentic AI Bible](https://www.amazon.es/Agentic-Bible-Up-Date-Goal-Driven-ebook/dp/B0FJ9QGK8S/)
- [An Illustrated Guide to AI Agents](https://learning.oreilly.com/library/view/an-illustrated-guide/9798341662681/)
- [Generative AI for Software Development](https://learning.oreilly.com/library/view/generative-ai-for/9781098162269/)
- [Context Engineering for Multi-Agent Systems](https://www.packtpub.com/en-us/product/context-engineering-for-multi-agent-systems-9781806690046)
- [AI Agents: The Definitive Guide](https://learning.oreilly.com/library/view/ai-agents-the/0642572247775/)

### AI for software development

- [Conductors to Orchestrators: The Future of Agentic Coding](https://addyo.substack.com/p/conductors-to-orchestrators-the-future)
- [The reality of AI-Assisted software engineering productivity](https://addyo.substack.com/p/the-reality-of-ai-assisted-software)
- [Vibe coding is not the same as AI-Assisted engineering](https://addyo.substack.com/p/vibe-coding-is-not-the-same-as-ai)
- [Coding for the Future Agentic World](https://addyo.substack.com/p/coding-for-the-future-agentic-world)
- [The AI-Native Software Engineer](https://substack.com/home/post/p-165160941)

### Other similar GitHub repositories

- [AI Engineering](https://github.com/chiphuyen/aie-book/)
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
- [Awesome LLM Apps](https://github.com/Shubhamsaboo/awesome-llm-apps)
- [Context Engineering (by David Kim)](https://github.com/davidkimai/Context-Engineering)
- [Context Engineering Template](https://github.com/coleam00/context-engineering-intro)
- [Awesome-Context-Engineering](https://github.com/Meirtz/Awesome-Context-Engineering)
- [AI Engineering Toolkit](https://github.com/Sumanth077/ai-engineering-toolkit)
- [Context Engineering for Multi-Agent Systems](https://github.com/Denis2054/Context-Engineering-for-Multi-Agent-Systems)
- [Agents Towards Production](https://github.com/NirDiamant/agents-towards-production)
- [Awesome generative AI guide](https://github.com/aishwaryanr/awesome-generative-ai-guide)
- [Generative AI for beginners](https://github.com/microsoft/generative-ai-for-beginners)
- [Best AI and LLM Engineering Resources](https://github.com/javabuddy/best-ai-and-llm-engineering-resource)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
- [Top GitHub Context Engineering repositories](https://github.com/topics/context-engineering)
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
- [Brex's prompt engineering guide](https://github.com/brexhq/prompt-engineering)

### Papers

- Mei, Lingrui, Jiayu Yao, Yuyao Ge, Yiwei Wang, Baolong Bi, Yujun Cai, Jiazhi Liu et al. "[A Survey of Context Engineering for Large Language Models](https://arxiv.org/abs/2507.13334)." arXiv preprint arXiv:2507.13334 (2025).
- Hua, Qishuo, Lyumanshan Ye, Dayuan Fu, Yang Xiao, Xiaojie Cai, Yunze Wu, Jifan Lin, Junfei Wang, and Pengfei Liu. "[Context Engineering 2.0: The Context of Context Engineering](https://arxiv.org/abs/2510.26493)." arXiv preprint arXiv:2510.26493 (2025).
- Zhang, Qizheng, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton et al. "[Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618)." arXiv preprint arXiv:2510.04618 (2025).


## Contributing

Any comments or feedback are more than welcome. Also, if you think something can be improved or want to contribute to this repo, please open a [pull request](https://github.com/bonigarcia/context-engineering/pulls).

## About

context-engineering (Copyright &copy; 2025) is an open-source project created and maintained by [Boni Garcia](https://bonigarcia.dev/), licensed under the terms of [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).