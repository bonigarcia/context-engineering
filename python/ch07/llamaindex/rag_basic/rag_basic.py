import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents from the 'data' directory
documents = SimpleDirectoryReader(".").load_data()

# Create a VectorStoreIndex from the documents
index = VectorStoreIndex.from_documents(documents)

# Create a query engine
query_engine = index.as_query_engine()

# Query the index
response = query_engine.query("What is LlamaIndex?")

# Print the response
print(response.response)
