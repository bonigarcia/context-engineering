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

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

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
    vectorstore = InMemoryVectorStore.from_documents(documents, embeddings)

    # 2. Create a base retriever
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 2}) # Retrieve top 2 documents

    # 3. Initialize the LLM for compression
    llm = ChatOpenAI(api_key=api_key, model="gpt-5-mini", temperature=0)

    # 4. Build an LLM-based extractor with LangChain Expression Language
    extractor_prompt = ChatPromptTemplate.from_template(
        """Extract verbatim the parts of the text below that are relevant to
the question. Do not add words of your own. Return an empty string if no
part of the text is relevant.

Question: {question}

Text:
{text}"""
    )
    extractor = extractor_prompt | llm | StrOutputParser()

    # 5. Wrap retrieval and extraction into a single compression retriever
    def compress(payload):
        docs = payload["documents"]
        extracted = extractor.batch(
            [{"question": payload["question"], "text": d.page_content} for d in docs]
        )
        return [
            Document(page_content=text.strip(), metadata=doc.metadata)
            for doc, text in zip(docs, extracted)
            if text.strip()
        ]

    compression_retriever = (
        RunnableLambda(
            lambda q: {"question": q, "documents": base_retriever.invoke(q)}
        )
        | RunnableLambda(compress)
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
