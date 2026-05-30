# Context engineering ![](https://bonigarcia.dev/img/context-engineering.png)

**Context engineering** can be defined as the practice of designing systems that provide a Large Language Model (LLM) and AI agents with all the necessary information to complete a task effectively. It goes beyond prompt engineering since it focuses on building a comprehensive and structured context from various sources like instructions, external knowledge, memory, tools, and state. The central idea is that the success of a complex LLM-based system depends more on the quality and completeness of the context provided than on the specific wording of the prompt itself.

Tobi Lütke, the CEO of Shopify, coined the term _context engineering_ in a [tweet](https://x.com/tobi/status/1935533422589399127) on June 19, 2025. He defined context engineering as _the art of providing all the context for the task to be plausibly solvable by the LLM_. This novel concept captures the essence of the current evolution of LLM-based systems, inspiring others (like me) to understand and define this emerging discipline. Since then, I've been working on a book entitled **Context Engineering: Building Consistent, Accurate, Predictable AI Systems**, to be published by [Manning](https://www.manning.com/) in 2026.

This GitHub repository is intended to be a companion resource for this book and a reference for practitioners looking to understand and adopt the context engineering principles.

_Warning_: This repository is a work in progress, so content and structure may change.

## Table of contents

This book aims to provide a strong, general-purpose theoretical foundation for context engineering, supported by hands-on examples. Its table of contents is the following:

1. Introduction to context engineering
2. Instructions in AI agents
3. External knowledge and retrieval
4. Tools in AI agents
5. Memory and state in agentic systems
6. User prompts for LLMs
7. Context management and orchestration
8. Evaluation and observability
9. Governance and operations
10. AI frameworks for context engineering
11. Context engineering for software development
12. State of the art on context engineering  
Appendix A. The AI ecosystem  
Appendix B. References and further reading

Each chapter of this book begins by explaining the underlying principles and patterns of each thematic block. The final part of each chapter then presents specific examples, all of which are available in this GitHub repository. New examples will continue to be added, and existing ones maintained, even after the book is published. The goal is to provide an open-source, up-to-date reference for everyone interested in context engineering.

## Examples

This repository organizes examples by chapter to help you explore context engineering concepts in practice.

#### Chapter 1. Introduction to context engineering
This chapter provides the foundations for interacting with different model providers:
- Basic interaction (OpenAI): [Python](./ch01/python/openai-gpt-basic) · [Jupyter](./ch01/jupyter/openai-gpt-basic.ipynb) · [JavaScript](./ch01/javascript/openai-gpt-basic) · [Java](./ch01/java/src/main/java/io/github/bonigarcia/ce/OpenAiGptBasic.java)
- Basic interaction (Anthropic): [Python](./ch01/python/anthropic-claude-basic) · [Jupyter](./ch01/jupyter/anthropic-claude-basic.ipynb) · [JavaScript](./ch01/javascript/anthropic-claude-basic) · [Java](./ch01/java/src/main/java/io/github/bonigarcia/ce/AnthropicClaudeBasic.java)
- Basic interaction (Google): [Python](./ch01/python/google-gemini-basic) · [Jupyter](./ch01/jupyter/google-gemini-basic.ipynb) · [JavaScript](./ch01/javascript/google-gemini-basic) · [Java](./ch01/java/src/main/java/io/github/bonigarcia/ce/GoogleGeminiBasic.java)
- Basic interaction (Ollama): [Python](./ch01/python/ollama-local-basic) · [Jupyter](./ch01/jupyter/ollama-local-basic.ipynb) · [JavaScript](./ch01/javascript/ollama-local-basic) · [Java](./ch01/java/src/main/java/io/github/bonigarcia/ce/OllamaLocalBasic.java)

#### Chapter 2. Instructions in AI agents
This chapter covers the definition and usage of instructions (system prompts, agent skills, instructions artifacts) as a foundation layer to shape the model behavior:
- System prompts (OpenAI): [Python](./ch02/python/openai-gpt-system-prompt) · [Jupyter](./ch02/jupyter/openai_gpt_system_prompt.ipynb) · [JavaScript](./ch02/javascript/openai-gpt-system-prompt) · [Java](./ch02/java/src/main/java/io/github/bonigarcia/ce/OpenAiGptSystemPrompt.java)
- System prompts (Anthropic): [Python](./ch02/python/anthropic-claude-system-prompt) · [Jupyter](./ch02/jupyter/anthropic_claude_system_prompt.ipynb) · [JavaScript](./ch02/javascript/anthropic-claude-system-prompt) · [Java](./ch02/java/src/main/java/io/github/bonigarcia/ce/AnthropicClaudeSystemPrompt.java)
- System prompts (Google): [Python](./ch02/python/google-gemini-system-prompt) · [Jupyter](./ch02/jupyter/google_gemini_system_prompt.ipynb) · [JavaScript](./ch02/javascript/google-gemini-system-prompt) · [Java](./ch02/java/src/main/java/io/github/bonigarcia/ce/GoogleGeminiSystemPrompt.java)
- System prompts (Ollama): [Python](./ch02/python/ollama-local-system-prompt) · [Jupyter](./ch02/jupyter/ollama_local_system_prompt.ipynb) · [JavaScript](./ch02/javascript/ollama-local-system-prompt) · [Java](./ch02/java/src/main/java/io/github/bonigarcia/ce/OllamaLocalSystemPrompt.java)
- Agent skills: [project-notetaker](./ch02/agent-skills/project-notetaker)
- Instruction artifacts: [task-tracker](./ch02/python/instruction-artifacts)

#### Chapter 3. External knowledge and retrieval
This chapter explores different patterns for providing external knowledge to a model:
- Retrieval-Augmented Generation (RAG): [Python](./ch03/python/rag-openai) · [Jupyter](./ch03/jupyter/rag_openai.ipynb)
- Advanced RAG: [LangChain](./ch03/python/agentic-rag) · [Qdrant](./ch03/python/local-rag) · [PageIndex](./ch03/python/vectorless-rag-pageindex) · [RAGFlow](./ch03/python/ragflow-basic)
- Context stuffing: [Python](./ch03/python/context-stuffing-system-prompt) · [Jupyter](./ch03/jupyter/context_stuffing_system_prompt.ipynb)
- Cache-Augmented Generation (CAG): [Python](./ch03/python/cag) · [Jupyter](./ch03/jupyter/cag.ipynb)
 
#### Chapter 4. Tools in AI agents
This chapter focuses on extending the capabilities of AI agents through tools:
- Function calling: [Python](./ch04/python/function_calling) · [JavaScript](./ch04/javascript/function_calling) · [Java](./ch04/java/function_calling)
- Command-Line Interface (CLI): [workspace-analyzer](./ch04/agent-skills/workspace-analyzer)
- Model Context Protocol (MCP) server: [Python](./ch04/python/mcp_server) · [JavaScript](./ch04/javascript/mcp_server) · [Java](./ch04/java/mcp_server)

#### Chapter 5. Memory and state in agentic systems
This chapter explores how to maintain information across interactions using memory and state:
- Session memory: [Python](./ch05/python/session_memory_chat)
- Long-term memory (Mem0): [Python](./ch05/python/mem0_chat) · [JavaScript](./ch05/javascript/mem0_chat) · [Java](./ch05/java/src/main/java/io/github/bonigarcia/ce/Mem0Chat.java)
- Long-term memory (Cognee): [Python](./ch05/python/cognee_memory)
- Memory coach: [Python](./ch05/python/memory_coach)
- Session state: [Python](./ch05/python/session_state_chat) · [JavaScript](./ch05/javascript/session_state_chat) · [Java](./ch05/java/src/main/java/io/github/bonigarcia/ce/SessionStateChat.java)
- Workflow state: [Python](./ch05/python/workflow_state_handoff) · [JavaScript](./ch05/javascript/workflow_state_handoff) · [Java](./ch05/java/src/main/java/io/github/bonigarcia/ce/WorkflowStateHandoff.java)

#### Chapter 6. User prompts for LLMs
This chapter focuses on the design and optimization of user prompts, including techniques like few-shot prompting, prompt chaining, Chain-of-Thought, or ReAct:
- Few-shot prompting: [Python](./ch06/python/few-shot-ticket-normalizer) · [Jupyter](./ch06/jupyter/few-shot-ticket-normalizer.ipynb) · [JavaScript](./ch06/javascript/few-shot-ticket-normalizer) · [Java](./ch06/java/src/main/java/io/github/bonigarcia/ce/FewShotTicketNormalizer.java)
- Prompt chaining: [Python](./ch06/python/prompt-chaining-support-reply) · [Jupyter](./ch06/jupyter/prompt-chaining-support-reply.ipynb) · [JavaScript](./ch06/javascript/prompt-chaining-support-reply) · [Java](./ch06/java/src/main/java/io/github/bonigarcia/ce/PromptChainingSupportReply.java)
- Chain-of-Thought vs ReAct (DSPy): [Python](./ch06/python/dspy-cot-vs-react) · [Jupyter](./ch06/jupyter/dspy_cot_vs_react.ipynb)

#### Chapter 7. Context management and orchestration
This chapter focuses on managing and orchestrating context in complex agentic systems, including context compression, hierarchical context, or multi-agent patterns:

- Context compression (LLMLingua): [Python](./ch07/context-compression)
- Filesystem context (OpenViking): [Python](./ch07/openviking-filesystem)
- Collaborative agents (CrewAI): [Python](./ch07/crewai-crew)
- Multi-agent router (LangGraph): [Python](./ch07/multi-agent-router)
- Orchestration (DeepAgents): [Python](./ch07/deepagents-orchestration)
- Agent-to-Agent (A2A) communication: [Python](./ch07/a2a-example)

#### Chapter 8. Evaluation and observability
This chapter covers evaluation and observability for context-aware systems:

- Metrics (DeepEval): [Python](./ch08/metrics-deepeval)
- Evals (Promptfoo): [YAML](./ch08/evals-promptfoo)
- LLM-as-judge (Ragas): [Python](./ch08/llm-as-judge-ragas)
- Observability (Langfuse): [Python](./ch08/observability-langfuse)
- Observability (LangSmith): [Python](./ch08/observability-langsmith)

#### Chapter 9. Governance and operations
This chapter covers governance, human oversight, and operational patterns for context-aware systems:

- Automated PII redaction (Microsoft Presidio): [Python](./ch09/pii_presidio)
- Output validation (Pydantic): [Python](./ch09/output_validation)
- Bias detection (Fairlearn): [Python](./ch09/bias_detection)
- Human-in-the-loop: [Python](./ch09/human-in-the-loop)
- Model fine-tuning: [Python](./ch09/fine_tuning)
- AI gateway (LiteLLM): [Python](./ch09/litellm_gateway)

## Online resources

This repository includes interactive web pages that complement the book and help you apply context engineering concepts in practice.

### 1. AI Ecosystem

🔗 https://bonigarcia.dev/context-engineering/ai-ecosystem.html

Curated collection of the AI ecosystem:

- Browse model families, agents, frameworks, and tooling in one place
- Search across the appendix snapshot by name, feature, license, or pricing

This page is a companion index for the Appendix A and is designed to stay easy to maintain as the ecosystem changes.

---

### 2. Context-Aware Prompt Builder

🔗 https://bonigarcia.dev/context-engineering/context-aware-prompt-builder.html

Design, compare, and reuse structured prompts across multiple frameworks and AI models:

- Build prompts using established frameworks (10-step, COSTAR, CRISPE, RTF, etc.)
- Switch frameworks dynamically while preserving intent
- Import/export prompts as JSON
- Measure approximate context usage for different models
- Load curated prompt samples for common SDLC roles

This tool is especially useful for creating and iterating on prompts in a structured, repeatable way.

---

### 3. SDLC Prompt Library

🔗 https://bonigarcia.dev/context-engineering/sdlc_prompt_library.html

Browse a curated library of prompts organized around the software development lifecycle (SDLC), including roles for architect, developer, debugger, reviewer, refactorer, tester, and documenter:

- Explore prompts visually using a card-based interface
- Filter by framework (10-step, COSTAR, CRISPE, RTF)
- Inspect full structured prompts for each role
- Copy prompts directly for reuse or adaptation

This tool is designed as a reference library, helping you understand how structured prompts vary across roles and frameworks.

---

### 4. Further Reading

🔗 https://bonigarcia.dev/context-engineering/references.html

Searchable catalog of articles, books, repositories, tutorials, and other references related to context engineering, prompting, agents, and AI engineering: context engineering, AI agents, machine learning, prompt engineering, RAG, generative AI, MCP, AI-assisted development, LLMs, memory, retrieval, multi-agent systems.

## Contributing

If you think something should be improved or want to contribute to this repo, please open a [pull request](https://github.com/bonigarcia/context-engineering/pulls). Any comments or feedback are welcome.

## About

context-engineering (Copyright &copy; 2025-2026) is an open-source project created and maintained by [Boni Garcia](https://bonigarcia.dev/), licensed under the terms of [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
