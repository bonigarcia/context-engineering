# Conversational memory and state with LlamaIndex

This example demonstrates how LlamaIndex facilitates conversational memory, allowing an LLM-powered chatbot to maintain context across multiple turns of a conversation. This is crucial for building engaging and coherent interactive AI applications, as it enables the LLM to remember past interactions and user preferences, thus influencing its future responses.

This example uses LlamaIndex's condense-question chat mode to combine the new user query with the chat history into a single query for retrieval and synthesis, effectively managing the conversational state.

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

The script will simulate a conversation with a LlamaIndex-powered chatbot. You will observe how the chatbot remembers previous turns and uses that context to answer subsequent questions.
