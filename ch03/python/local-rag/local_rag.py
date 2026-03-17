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