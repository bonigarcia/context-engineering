import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# LangSmith specific environment variables
# Ensure these are set in your .env file or environment
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY="YOUR_LANGSMITH_API_KEY"
# LANGCHAIN_PROJECT="Your LangChain Project Name" # Optional, but good practice

if __name__ == "__main__":
    # Initialize the LLM
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)

    # Define a chat prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant that answers questions concisely."),
        ("user", "{input}")
    ])

    # Define an output parser
    output_parser = StrOutputParser()

    # Create a simple chain
    chain = prompt | llm | output_parser

    # Invoke the chain
    print("--- Invoking LangChain with LangSmith tracing enabled ---")
    question = "What is the capital of Canada?"
    response = chain.invoke({"input": question})

    print(f"Question: {question}")
    print(f"Answer: {response}")

    print("
--- To view the trace, visit your LangSmith project dashboard ---")
    print("Ensure LANGCHAIN_TRACING_V2=true and LANGCHAIN_API_KEY are set.")
    if os.getenv("LANGCHAIN_PROJECT"):
        print(f"Look for a run in project: {os.getenv('LANGCHAIN_PROJECT')}")
    else:
        print("Default project name will be 'default'.")
