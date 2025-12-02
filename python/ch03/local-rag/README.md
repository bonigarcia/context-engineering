## Local retrieval-augmented generation (RAG)

This sample application implements a local RAG system using the following stack:

- LLM: [Llama 3.2 1B](https://ollama.com/library/llama3.2:1b) via [Ollama](https://ollama.com/download)
- Embedding model: [OpenHermes](https://ollama.com/library/openhermes) (embedder for OllamaEmbedder)
- Vector database: [Qdrant](https://qdrant.tech/)
- Agent framework: [Agno](https://github.com/agno-agi/agno)

### Requirements

To run this example, you need the following:

- [Python](https://www.python.org/), for  the local RAG.
- [Ollama](https://ollama.com/), for the LLM and the embedding model.
- [Docker](https://www.docker.com/), for the vector database.
- [Node.js](https://nodejs.org/), for the agent web interface.

### Steps for running this example

1. Pull Llama 3.2 1B and OpenHermes with Ollama:
```bash
ollama pull llama3.2:1b
ollama pull openhermes
```

2. Pull and install Qdrant with Docker:
```bash
docker pull qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant
```

3. Get the Python sources and install dependencies (using a virtual environment is recommended):
```bash
git clone https://github.com/bonigarcia/context-engineering
cd context-engineering/python/ch03/local-rag
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Run the RAG Agent. Check that the agent API interface is working at http://localhost:7777/
```bash
python local_rag.py
```

5. Install a web interface. Open the UI interface and interact with the agent at http://localhost:3000/
```bash
npx create-agent-ui@latest
cd agent-ui
npm install
npm run dev
```

![RAG UI interface](/docs/img/loca-rag-ui.png)
