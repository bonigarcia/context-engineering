from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_classic.agents.agent import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_core.tools import create_retriever_tool
from langchain_classic import hub
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Set up the vector store
documents = [
    "The author of the book 'Fake Book: The New Age' is George Cauldron.",
    "The book discusses techniques for building robust and reliable AI systems.",
]
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.from_texts(documents, embeddings)
retriever = vector_store.as_retriever()

# 2. Create the RAG tool
tool = create_retriever_tool(
    retriever,
    "search_documents",
    "Searches and returns documents.",
)
tools = [tool]

# 3. Create the agent
prompt = hub.pull("hwchase17/react") # A pre-built ReAct prompt
llm = OllamaLLM(model="llama3.2:3b")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# 4. Run the agent with some questions
def run_agent(question):
    try:
        response = agent_executor.invoke({"input": question})
        print(response["output"])
    except Exception as e:
        print(f"An error occurred: {e}")

question = "Who is the author of the book 'Fake Book: The New Age'?"
print(question)
run_agent(question)
