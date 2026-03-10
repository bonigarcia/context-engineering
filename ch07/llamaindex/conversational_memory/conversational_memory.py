import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.llms.openai import OpenAI

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

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
