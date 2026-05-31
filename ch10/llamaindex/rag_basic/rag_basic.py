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
