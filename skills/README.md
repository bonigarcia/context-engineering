# Agent skills for context engineering

This folder contains a collection of [agent skills](https://agentskills.io/) that apply the methods of the book [Context Engineering](https://hubs.la/Q04ksQ8J0) (Manning) to your own AI agents and LLM applications. Each skill reviews one artifact you already have (an AGENTS.md file, a set of tool definitions, a RAG pipeline, the context of an agent) and returns a structured report of findings, each one linked to the book section that explains it.

These skills are tools that act on your project. If you are looking for skills that teach an agent the principles of context engineering, see the excellent [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) collection by Muratcan Koylan, which complements this one.

A browsable catalog of these skills is available at https://bonigarcia.dev/context-engineering/agent-skills.html.

## Skills

| Skill | Chapter | What it reviews |
|---|---|---|
| [instruction-auditor](./instruction-auditor) | 2. Instructions for AI agents | A system prompt or an instruction artifact such as AGENTS.md or CLAUDE.md |
| [skill-reviewer](./skill-reviewer) | 2. Instructions for AI agents | A skill directory with a SKILL.md file |
| [retrieval-advisor](./retrieval-advisor) | 3. External knowledge and retrieval | A RAG pipeline (code and configuration) or a description of a knowledge source |
| [tool-reviewer](./tool-reviewer) | 4. Tools in AI agents | Function-calling tool schemas or an MCP server |
| [memory-designer](./memory-designer) | 5. Memory and state in agentic systems | A description or the code of an agent |
| [prompt-reviewer](./prompt-reviewer) | 6. User prompts for LLMs | User prompt templates, few-shot examples, or prompt chains |
| [token-budget-auditor](./token-budget-auditor) | 7. Context management and orchestration | The files and prompts that make up an agent's context |
| [eval-builder](./eval-builder) | 8. Evaluation and observability | A description or the code of an agent or prompt |
| [governance-check](./governance-check) | 9. Governance and operations | An agent's tools, instructions, and data flows |

## Installation

### As a plugin

The repository is a plugin for Claude Code and Codex. In Claude Code:

```
/plugin marketplace add bonigarcia/context-engineering
/plugin install context-engineering-skills@context-engineering
```

In Codex, add the repository as a plugin source and install `context-engineering-skills` from the plugin browser (`/plugins`).

### Manually

Each skill is a self-contained folder, so you can copy only the skills you need. Clone the repository and copy a skill folder into the location your agent scans:

| Agent | Project level | User level |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex and other agents that follow the Agent Skills specification | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `.cursor/skills/` | See the Cursor documentation |

For example, to add the tool reviewer to a project for Claude Code:

```bash
git clone https://github.com/bonigarcia/context-engineering.git
mkdir -p your-project/.claude/skills
cp -r context-engineering/skills/tool-reviewer your-project/.claude/skills/
```

Two skills include Python scripts (`skill-reviewer` and `token-budget-auditor`). They need Python 3.10 or later and no extra packages. `token-budget-auditor` uses `tiktoken` for exact counts when it is installed, and a character-based estimate otherwise.

## Using the skills

Ask your agent for the task in your own words, for example "review the tools of this MCP server" or "audit our AGENTS.md". The agent activates the matching skill from its description. You can also invoke a skill directly when your agent supports it, for example `/tool-reviewer` in Claude Code.

Every skill returns the same kind of report: a summary, a list of findings (severity, location, problem, suggested fix, and book section), any skill-specific section (such as a token table or a set of evaluation cases), and a final JSON block with the same content, so that other tools or skills can consume the results.

Each skill folder has an `examples/` folder with a flawed sample artifact and an `expected-findings.md` file. They are a quick way to see what a skill does, and they are the test cases of the evaluation harness.

## Evaluation

The [evals](./evals) folder contains a [Promptfoo](https://github.com/promptfoo/promptfoo) harness that checks that each skill finds the expected problems in its sample artifact and that each description makes an agent pick the right skill. See [evals/README.md](./evals/README.md).

## Repository tooling

The [_tools](./_tools) folder contains the script that generates the catalog data of the web page (`python3 skills/_tools/build_catalog.py`, run from the repository root after changing any skill) and its tests. Skills do not depend on it.
