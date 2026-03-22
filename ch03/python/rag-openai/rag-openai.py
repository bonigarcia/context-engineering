import os
import textwrap
from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

# 1. Setup
client = OpenAI()

# 2. Knowledge base
documents: List[Dict[str, str]] = [
    {
        "id": "guide_sync",
        "title": "Syncing notes across devices",
        "text": """LumaNote automatically synchronizes your notes across all signed-in devices.
To enable sync, sign in with the same account on each device and keep the "Cloud sync" toggle turned on in Settings → Sync.
Sync uses end-to-end encryption. LumaNote servers cannot read your note contents.
Sync runs every few seconds when you are online. Large attachments may take longer to upload."""
    },
    {
        "id": "guide_offline",
        "title": "Offline mode and local cache",
        "text": """When you lose network connectivity, LumaNote switches to offline mode.
You can continue creating and editing notes while offline. Changes are stored in a local cache.
When the connection is restored, LumaNote reconciles offline changes and uploads them to the cloud.
If the same note was edited on two devices while offline, you will be asked which version to keep."""
    },
    {
        "id": "guide_sharing",
        "title": "Sharing notes with teammates",
        "text": """You can share a note with teammates by clicking the Share button in the top-right corner.
Add teammates by email address and choose whether they can view or edit.
Shared notes show an avatar for each active collaborator. Changes appear in real time for everyone."""
    },
]

# 3. Retriever (TF-IDF)
corpus = [doc["text"] for doc in documents]
vectorizer = TfidfVectorizer(stop_words="english")
doc_vectors = vectorizer.fit_transform(corpus)

def retrieve(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """Retrieve the top-k most similar documents to the query."""
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, doc_vectors)[0]
    top_indices = np.argsort(similarities)[::-1][:k]

    results: List[Dict[str, Any]] = []
    for idx in top_indices:
        results.append({
            "id": documents[idx]["id"],
            "title": documents[idx]["title"],
            "score": float(similarities[idx]),
            "text": documents[idx]["text"],
        })
    return results

# 4. Prompt construction
def build_context(docs: List[Dict[str, Any]]) -> str:
    """Format retrieved documents into a context block for the model."""
    parts = []
    for i, d in enumerate(docs, start=1):
        parts.append(f"[Document {i}: {d['title']}]\n{d['text'].strip()}")
    return "\n\n".join(parts)

# 5. RAG Pipeline
def query_model_with_rag(question: str, k: int = 3, model: str = "gpt-4o-mini", show_sources: bool = True) -> str:
    """Answer a question using a simple RAG pipeline."""
    retrieved_docs = retrieve(question, k=k)
    context = build_context(retrieved_docs)

    if show_sources:
        print("\n[Retrieved passages]")
        for d in retrieved_docs:
            snippet = textwrap.shorten(d["text"], width=100, placeholder="...")
            print(f"- {d['title']} (score={d['score']:.3f}): {snippet}")

    prompt = (
        "You are a helpful assistant answering questions about the note-taking app LumaNote.\n"
        "Use ONLY the information in the documentation below to answer the question.\n"
        "If the answer is not contained in the documentation, say that you do not know.\n\n"
        "Documentation:\n"
        f"{context}\n\n"
        f"User question: {question}"
    )

    # Note: Using the modern Responses API if available, or fallback to Chat Completions
    try:
        response = client.responses.create(
            model=model,
            input=prompt,
        )
        return response.output[0].content[0].text
    except AttributeError:
        # Fallback to standard chat completions if 'responses' is not available
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    question = "How can I sync my notes between my phone and laptop?"
    print(f"Question: {question}")
    
    answer = query_model_with_rag(question)
    print(f"\nAnswer:\n{answer}")
