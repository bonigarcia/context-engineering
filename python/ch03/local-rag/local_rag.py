import asyncio
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.os import AgentOS

# Knowledge base
vector_db = Qdrant(
    collection="my-vector-db",
    url="http://localhost:6333",
    embedder=OllamaEmbedder(),
)

knowledge_base = Knowledge(
    vector_db=vector_db,
)

# Agent
agent = Agent(
    name="Local RAG",
    model=Ollama(id="llama3.2:1b"),
    knowledge=knowledge_base,
)
agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()

async def init_knowledge():
    """Ingest external knowledge (PDF documents)"""
    await knowledge_base.add_content_async(
        url="https://bonigarcia.dev/webdrivermanager/webdrivermanager.pdf",
        name="WebDriverManager manual",
        skip_if_exists=True,
    )

if __name__ == "__main__":
    # Ingest external knowledge before starting the server
    asyncio.run(init_knowledge())

    # Start the AgentOS app
    agent_os.serve(app="local_rag:app", reload=True)
