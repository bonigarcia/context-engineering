# RAGFlow Basic Example

This example demonstrates how to use the RAGFlow Python SDK to create a dataset, a chat assistant, and start a conversation.

[RAGFlow](https://github.com/infiniflow/ragflow) is an open-source RAG engine based on deep document understanding. It offers a streamlined workflow for businesses of any size to extract knowledge from complex data and provide accurate answers with rigorous citations.

## Prerequisites

* [Python](https://www.python.org/) 3.10+
* [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
* A running RAGFlow instance (see instructions below)

## Steps for running RAGFlow with Docker

1. Clone the RAGFlow repository:
```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker
# Recommended: checkout a specific stable version
# git checkout -f v0.24.0
```

2. Start the RAGFlow server:
```bash
docker compose up -d
```

3. Access the RAGFlow UI at `http://localhost`.
4. Generate an API key: Click your avatar in the top right → API → Create API Key.

## Steps for running this example in the shell

1. Install dependencies:
```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Configure environment variables in a `.env` file:
```env
RAGFLOW_API_KEY="your_api_key_here"
RAGFLOW_BASE_URL="http://localhost:9380"
```

3. Run the script:
```bash
python ragflow_example.py
```

## Output

The script will initialize the client, create a dataset and assistant, and perform a basic query.

```
Creating dataset 'MyQuickstartDataset' using model: gemini-embedding-001@Google...
Dataset created: MyQuickstartDataset(4) (ID: 9e9e7e362c3f11f1863791b66733cdba)
Uploading document: C:\Users\boni\Documents\dev\context-engineering\ch03\python\ragflow-basic\ragflow_example.py...
Uploaded document IDs: ['9ea57e202c3f11f1863791b66733cdba']
Starting parsing... this may take a minute.
Parsing complete.
Creating chat assistant 'MyAssistant_1774878721'...
Assistant created: MyAssistant_1774878721
Starting conversation...
Asking: What does the 'main' function do in the uploaded script?
Assistant: The `main` function in the uploaded script initializes a RAGFlow client, creates a dataset, uploads a document (the script itself), parses the document, creates a chat assistant, and starts a conversation by asking a question about the script [ID:0] [ID:1]. It also includes error handling [ID:0].
```
