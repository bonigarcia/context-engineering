import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

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
    "Given the following information, please answer the question below:"
    "---------------------"
    "{context_str}"
    "---------------------"
    "Question: {query_str}"
    "Your concise answer: "
)

# Configure the LLM and Embedding Model
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.0)
embed_model = OpenAIEmbedding()

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
