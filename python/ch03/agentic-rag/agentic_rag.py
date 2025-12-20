from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.agents.agent import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_core.tools import create_retriever_tool
from langchain_classic import hub

# 1. Set up the vector store
documents = [
    "The author of the book 'Context Engineering for Generative AI' is Boni Garcia.",
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
prompt = hub.pull("hwchase17/react")
llm = Ollama(model="llama3.2:1b")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. Run the agent with some questions
def run_agent(question):
    try:
        response = agent_executor.invoke({"input": question})
        print(response["output"])
    except Exception as e:
        print(f"An error occurred: {e}")

print("--- Question 1: Who is Boni Garcia? (Agent should use its own knowledge) ---")
run_agent("Who is Boni Garcia?")

print("\n--- Question 2: Who is the author of the book 'Context Engineering for Generative AI'? (Agent should use the RAG tool) ---")
run_agent("Who is the author of the book 'Context Engineering for Generative AI'?")
