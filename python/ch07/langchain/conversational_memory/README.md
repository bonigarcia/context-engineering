# Conversational memory with LangChain

This example demonstrates how to implement conversational memory in LangChain, allowing an LLM to retain context from previous turns in a dialogue. It utilizes `ConversationBufferMemory` to store chat messages and inject them into subsequent prompts, enabling more coherent and context-aware interactions.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```
Alternatively, create a `.env` file in the source directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

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
