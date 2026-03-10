import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

if __name__ == "__main__":
    # Sample documents (more verbose than needed to show compression benefit)
    documents = [
        Document(page_content="The cat sat on the mat. It was a fluffy cat.", metadata={"source": "doc1"}),
        Document(page_content="The dog chased the ball. The ball was red and bounced high.", metadata={"source": "doc2"}),
        Document(page_content="Contextual compression reduces the noise in retrieved documents. This helps LLMs focus on relevant information. It's especially useful when the retrieved chunks contain a lot of irrelevant detail around the answer.", metadata={"source": "doc3"}),
        Document(page_content="LangChain provides tools like LLMChainExtractor for post-processing retrieved documents to make them more concise and relevant to the query.", metadata={"source": "doc4"}),
        Document(page_content="A bird flew south for the winter. It was a robin. Robins are migratory birds.", metadata={"source": "doc5"}),
    ]

    # 1. Create embeddings and a vector store
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vectorstore = FAISS.from_documents(documents, embeddings)

    # 2. Create a base retriever
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 2}) # Retrieve top 2 documents

    # 3. Initialize the LLM for compression
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)

    # 4. Create a document compressor using an LLM
    # LLMChainExtractor extracts relevant passages from documents
    compressor = LLMChainExtractor.from_llm(llm)

    # 5. Create a ContextualCompressionRetriever
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )

    query = "What is contextual compression in LangChain?"

    print(f"Query: {query}")

    # Retrieve with base retriever
    print("--- Retrieved documents (without compression) ---")
    retrieved_docs_raw = base_retriever.invoke(query)
    for i, doc in enumerate(retrieved_docs_raw):
        print(f"Document {i+1} (Source: {doc.metadata.get('source', 'N/A')}):{doc.page_content}---")

    # Retrieve with compression retriever
    print("--- Retrieved documents (with contextual compression) ---")
    compressed_docs = compression_retriever.invoke(query)
    for i, doc in enumerate(compressed_docs):
        print(f"Document {i+1} (Source: {doc.metadata.get('source', 'N/A')}):{doc.page_content}---")

    # Example of using compressed docs with an LLM (simplified)
    print("--- LLM response using compressed context (conceptual) ---")
    qa_prompt = ChatPromptTemplate.from_template("""Answer the question based on the following context:
    {context}

    Question: {question}""")
    
    # Combine compressed documents into a single string for the prompt
    context_str = "".join([d.page_content for d in compressed_docs])
    
    response_chain = qa_prompt | llm | StrOutputParser()
    llm_response = response_chain.invoke({"context": context_str, "question": query})
    print(llm_response)
