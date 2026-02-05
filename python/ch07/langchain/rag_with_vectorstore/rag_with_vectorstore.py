import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter # Updated import
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

if __name__ == "__main__":
    # Create a dummy document for demonstration
    # In a real application, you would load from an actual file or database
    document_content = """
    The quick brown fox jumps over the lazy dog.
    This is a sample document for demonstrating Retrieval-Augmented Generation (RAG).
    RAG combines the power of large language models with external knowledge bases.
    It allows LLMs to retrieve relevant information and use it to generate more accurate and up-to-date responses.
    LangChain provides various components to build RAG applications, including document loaders, text splitters, embedding models, vector stores, and retrievers.
    FAISS is a library for efficient similarity search and clustering of dense vectors.
    """
    # Define the path where the dummy document will be created
    dummy_doc_path = "sample_document.txt"
    with open(dummy_doc_path, "w") as f:
        f.write(document_content)

    # 1. Load the document
    loader = TextLoader(dummy_doc_path)
    docs = loader.load()

    # 2. Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 3. Create embeddings and a vector store
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vectorstore = FAISS.from_documents(splits, embeddings)

    # 4. Create a retriever
    retriever = vectorstore.as_retriever()

    # 5. Define a prompt for RAG
    rag_prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
    <context>
    {context}
    </context>
    Question: {input}""")

    # 6. Initialize the LLM
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)

    # 7. Create a chain to combine documents
    combine_docs_chain = create_stuff_documents_chain(llm, rag_prompt)

    # 8. Create the retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    # 9. Invoke the retrieval chain with a query
    query = "What is RAG and why is it useful?"
    response = retrieval_chain.invoke({"input": query})

    print(f"Query: {query}")
    print(f"Response: {response['answer']}")
    print(f"Source Documents: {[doc.metadata for doc in response['context']]}")

    # Clean up the dummy document
    os.remove(dummy_doc_path)
