# Conversational memory with LangChain

This example demonstrates how to implement conversational memory in LangChain, allowing an LLM to retain context from previous turns in a dialogue. It utilizes `ConversationBufferMemory` to store chat messages and inject them into subsequent prompts, enabling more coherent and context-aware interactions.

## Requirements

* [Python](https://www.python.org/) 3.10+
* An [OpenAI API key](https://platform.openai.com/api-keys) set as an environment variable (`OPENAI_API_KEY`)

## Steps for running this example in the shell

1. Install dependencies:
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

2. Export your API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python conversational_memory.py
```

## Output

When you run the script, it will simulate a short conversation with an LLM. The output will show each turn of the conversation, along with the AI's response and the accumulated chat history maintained by `ConversationBufferMemory`. You will observe how the LLM uses the past conversation to inform its answers.

Example output:

```
--- Conversation Turn 1 ---
User: Hi there! What's your name?
AI: I am an AI assistant. You can call me Assistant.
Current History: [HumanMessage(content='Hi there! What's your name?'), AIMessage(content='I am an AI assistant. You can call me Assistant.')]

--- Conversation Turn 2 ---
User: What did I just ask you?
AI: You asked me what my name is.
Current History: [HumanMessage(content='Hi there! What's your name?'), AIMessage(content='I am an AI assistant. You can call me Assistant.'), HumanMessage(content='What did I just ask you?'), AIMessage(content='You asked me what my name is.')]

--- Conversation Turn 3 ---
User: And what is your name again?
AI: My name is Assistant.
Current History: [HumanMessage(content='Hi there! What's your name?'), AIMessage(content='I am an AI assistant. You can call me Assistant.'), HumanMessage(content='What did I just ask you?'), AIMessage(content='You asked me what my name is.'), HumanMessage(content='And what is your name again?'), AIMessage(content='My name is Assistant.')]
```
