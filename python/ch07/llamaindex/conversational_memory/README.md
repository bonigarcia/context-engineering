# Conversational memory and state with LlamaIndex

This example demonstrates how LlamaIndex facilitates conversational memory, allowing an LLM-powered chatbot to maintain context across multiple turns of a conversation. This is crucial for building engaging and coherent interactive AI applications, as it enables the LLM to remember past interactions and user preferences, thus influencing its future responses.

The `CondenseQuestionChatEngine` is used here to condense the new user query with the chat history into a single query for retrieval and synthesis, effectively managing the conversational state.


## Requirements

* [Python](https://www.python.org/) 3.8+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

3. Run the script:
```bash
python conversational_memory.py
```

## Output

The script will simulate a conversation with a LlamaIndex-powered chatbot. You will observe how the chatbot remembers previous turns and uses that context to answer subsequent questions.
