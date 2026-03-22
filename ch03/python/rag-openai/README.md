# RAG with OpenAI

This example demonstrates a basic Retrieval-Augmented Generation (RAG) pipeline using OpenAI models and local TF-IDF retrieval.

The example uses a fictional documentation corpus for a note-taking app called *LumaNote* and shows how the model can ground its answers in these documents.

## Requirements

* [Python](https://www.python.org/) 3.6+
* An [OpenAI API key](https://platform.openai.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python rag-openai.py
```

## Output

The script will retrieve relevant documentation fragments and then call the OpenAI model to answer a question about syncing notes.

```
Question: How can I sync my notes between my phone and laptop?

[Retrieved passages]
- Syncing notes across devices (score=0.620): LumaNote automatically synchronizes your notes across all signed-in devices. To enable sync, sign...
- Sharing notes with teammates (score=0.059): You can share a note with teammates by clicking the Share button in the top-right corner. Add...
- Offline mode and local cache (score=0.047): When you lose network connectivity, LumaNote switches to offline mode. You can continue creating...

Answer:
To sync your notes between your phone and laptop using LumaNote, sign in with the same account on both devices and ensure that the "Cloud sync" toggle is turned on in Settings → Sync. LumaNote will automatically synchronize your notes across all signed-in devices.
```
