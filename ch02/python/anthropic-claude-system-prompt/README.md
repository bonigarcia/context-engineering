# System prompt with Anthropic Claude models

This example demonstrates how to set up an [Anthropic](https://anthropic.com/) Claude model and send a system prompt with Python.

## Requirements

* [Python](https://www.python.org/) 3.12+
* An [Anthropic API key](https://console.anthropic.com/settings/keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Export your Anthropic API key as an environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..." # Windows cmd: set ANTHROPIC_API_KEY="sk-ant-..." # Windows PowerShell: $env:ANTHROPIC_API_KEY="sk-ant-..."
```

3. Run the script:
```bash
python anthropic-claude-system-prompt.py
```

## Output

When you run the script, it will send a system prompt and a user prompt to the model, which should provide a response:

```
=== With system prompt ===
User query: Explain me what is context engineering in simple words
Response: "Please explain **to** me what context engineering is in simple words" — Context engineering is the practice of carefully designing and organizing the information you provide to an AI so that it fully understands the situation, rules, and goals needed to give you the best possible response.

=== With only user prompt ===
User query: Explain me what is context engineering in simple words
Response: # Context Engineering – Simple Explanation

## The Basic Idea

**Context engineering** is the practice of **carefully designing what information you give to an AI** so it performs better.

Think of it like this:

> 🧑‍🍳 You're giving instructions to a chef. *What* you tell them, *how* you tell them, and *what background info* you provide determines how good the meal turns out.

---

## A Simple Analogy

Imagine hiring a new employee:

| What you give them | Result |
|---|---|
| Just a task | Confused, generic work |
| Task + background + examples + rules | Great, targeted work |

**Context engineering = giving the AI the right "briefing"**

---

## What "Context" Includes

- 📋 **Instructions** – what you want the AI to do
- 🧠 **Background info** – relevant facts or documents
- 💬 **Examples** – showing good vs bad outputs
- 🗂️ **Memory** – past conversation or history
- 🎭 **Role** – telling AI who it should act as
- ⚠️ **Constraints** – what to avoid

---

## Why It Matters

- AI only knows what's **in its context window**
- Better context = **better, more accurate responses**
- It's becoming a core skill like **prompt engineering**, but broader

---

## One Line Summary

> **Context engineering = strategically feeding the right information to an AI at the right time to get the best results.**

Want a deeper dive into any part?
```
