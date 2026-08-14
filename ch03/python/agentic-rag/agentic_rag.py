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
from langchain.agents import create_agent
from langchain_core.tools import create_retriever_tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.vectorstores import InMemoryVectorStore

# 1. Set up the vector store
documents = [
    "The author of the book 'Fake Book: The New Age' is George Cauldron.",
    "The book discusses techniques for building robust and reliable AI systems.",
]
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = InMemoryVectorStore.from_texts(documents, embeddings)
retriever = vector_store.as_retriever()

# 2. Create the RAG tool
# The description is the only signal the agent has when it decides whether to
# retrieve, so it must state what the collection contains
tool = create_retriever_tool(
    retriever,
    "search_documents",
    "Search the private document collection, which contains facts about "
    "books, their authors, and their content. Use it for any question "
    "about a book or an author.",
)
tools = [tool]

# 3. Create the agent
# create_agent (LangChain 1.0+) builds the tool-calling loop internally, so no
# ReAct prompt and no AgentExecutor are needed. The model must support tool
# calling and have enough capacity to answer from the retrieved passages
llm = ChatOllama(model="llama3.1:8b", temperature=0)
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "Answer in one sentence, using only the passages returned "
        "by the search_documents tool."
    ),
)


# 4. Run the agent with some questions
def run_agent(question):
    try:
        response = agent.invoke(
            {"messages": [{"role": "user", "content": question}]}
        )
        print(response["messages"][-1].content)
    except Exception as e:
        print(f"An error occurred: {e}")


question = "Who is the author of the book 'Fake Book: The New Age'?"
print(question)
run_agent(question)
