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

if __name__ == "__main__":
    # Initialize the LLM
    llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)

    # Define a chat prompt template with a system message and user input
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Your name is {name}."),
        ("user", "{input}")
    ])

    # Define an output parser to get a string response
    output_parser = StrOutputParser()

    # Create a chain combining the prompt, LLM, and output parser
    chain = prompt | llm | output_parser

    # Invoke the chain with specific inputs
    response = chain.invoke({"name": "Bob", "input": "What is the capital of France?"})
    print(response)