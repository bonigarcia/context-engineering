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
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Create a dummy document
documents = [
    "The main character of the story is Alice. Alice lives in Wonderland."
]

# Load documents (in a real scenario, you'd load from files)
from llama_index.core.schema import Document
documents = [Document(text=d) for d in documents]

# Create a VectorStoreIndex from the documents
index = VectorStoreIndex.from_documents(documents)

# Initialize the LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.0)

# Create a chat engine with memory
chat_engine = index.as_chat_engine(
    chat_mode="condense_question",
    llm=llm,
    verbose=True
)

# Start a conversation
print("Chatbot: Hello! I know about Alice. What would you like to know?")

response = chat_engine.chat("Who is the main character?")
print(f"User: Who is the main character?")
print(f"Chatbot: {response.response}")

response = chat_engine.chat("Where does she live?")
print(f"User: Where does she live?")
print(f"Chatbot: {response.response}")

response = chat_engine.chat("Tell me more about her home.")
print(f"User: Tell me more about her home.")
print(f"Chatbot: {response.response}")
