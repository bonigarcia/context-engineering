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
from llama_index.core import VectorStoreIndex
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Create a dummy document
documents = [
    "The capital of France is Paris. Paris is known for its Eiffel Tower."
]

# Load documents (in a real scenario, you'd load from files)
# For this example, we'll create a Document object manually
from llama_index.core.schema import Document
documents = [Document(text=d) for d in documents]

# Create a VectorStoreIndex from the documents
index = VectorStoreIndex.from_documents(documents)

# Define custom system and query prompts
# System prompt: Provides high-level instructions to the LLM
custom_system_prompt = (
    "You are an expert Q&A system that always answers in the style of a helpful, "
    "concise, and informative assistant. Your answers should be brief and to the point."
)

# Query prompt: Guides the LLM on how to respond to user queries, incorporating retrieved context
custom_query_prompt = PromptTemplate(
    "Given the following information, please answer the question below:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Question: {query_str}\n"
    "Your concise answer: "
)

# Configure the LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.0)

# Create a query engine with custom prompts
query_engine = index.as_query_engine(
    system_prompt=custom_system_prompt,
    text_qa_template=custom_query_prompt,
    llm=llm
)

# Query the index with a specific question
response = query_engine.query("What is the capital of France?")

# Print the response
print(f"System Prompt: {custom_system_prompt}")
print(f"Query Prompt Template: {custom_query_prompt.template}")
print(f"Query: What is the capital of France?")
print(f"Response: {response.response}")

response = query_engine.query("Tell me about Paris.")
print(f"Query: Tell me about Paris.")
print(f"Response: {response.response}")
