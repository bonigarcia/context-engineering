import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents from the current directory
documents = SimpleDirectoryReader(".").load_data()

# Create a VectorStoreIndex from the documents
index = VectorStoreIndex.from_documents(documents)

# Create a query engine
query_engine = index.as_query_engine()

# Invoke a user query
response = query_engine.query("What is LlamaIndex?")

# Print the response
print(response.response)
