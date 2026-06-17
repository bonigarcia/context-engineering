"""
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

if __name__ == "__main__":
    # Initialize the LLM
    llm = ChatOpenAI(api_key=api_key, model="gpt-5-mini", temperature=0)

    # Define a chat prompt template with a system message, history, and user input
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])

    # Create a chain combining the prompt, LLM, and output parser
    chain = prompt | llm | StrOutputParser()

    # Initialize ConversationBufferMemory
    memory = ConversationBufferMemory(return_messages=True)

    # Simulate a conversation
    print("--- Conversation Turn 1 ---")
    input_text_1 = "Hi there! What's your name?"
    response_1 = chain.invoke({"input": input_text_1, "history": memory.load_memory_variables({})["history"]})
    print(f"User: {input_text_1}")
    print(f"AI: {response_1}")
    memory.save_context({"input": input_text_1}, {"output": response_1})
    print(f"Current History: {memory.load_memory_variables({})['history']}")

    print("--- Conversation Turn 2 ---")
    input_text_2 = "What did I just ask you?"
    response_2 = chain.invoke({"input": input_text_2, "history": memory.load_memory_variables({})["history"]})
    print(f"User: {input_text_2}")
    print(f"AI: {response_2}")
    memory.save_context({"input": input_text_2}, {"output": response_2})
    print(f"Current History: {memory.load_memory_variables({})['history']}")

    print("--- Conversation Turn 3 ---")
    input_text_3 = "And what is your name again?"
    response_3 = chain.invoke({"input": input_text_3, "history": memory.load_memory_variables({})["history"]})
    print(f"User: {input_text_3}")
    print(f"AI: {response_3}")
    memory.save_context({"input": input_text_3}, {"output": response_3})
    print(f"Current History: {memory.load_memory_variables({})['history']}")
