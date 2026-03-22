import numpy as np
import re
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 1. Knowledge base
DOCUMENTS = [
    {
        "id": "doc1",
        "title": "What is RAG?",
        "text": (
            "Retrieval-Augmented Generation (RAG) combines information retrieval with text generation. "
            "A retriever finds relevant passages from a knowledge base, and a generator uses those passages "
            "to produce an answer grounded in external sources."
        ),
    },
    {
        "id": "doc2",
        "title": "Chunking",
        "text": (
            "Chunking splits long documents into smaller passages. Overlapping chunks preserve context near boundaries. "
            "Fetching only the most relevant chunks keeps prompts short and focused."
        ),
    },
    {
        "id": "doc3",
        "title": "Similarity",
        "text": (
            "Cosine similarity measures closeness between vectors. With TF-IDF, we compare queries and chunks "
            "to retrieve the most relevant passages."
        ),
    },
    {
        "id": "doc4",
        "title": "Citations",
        "text": (
            "Providing citations to retrieved passages improves transparency and helps users verify answers. "
            "It reduces the risk of hallucinations by grounding claims in source text."
        ),
    },
]

# 2. Chunking
def simple_word_chunk(text: str, chunk_size: int = 50, overlap: int = 10) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start = end - overlap
    return chunks

KB_CHUNKS = []
for doc in DOCUMENTS:
    for i, ch in enumerate(simple_word_chunk(doc["text"], chunk_size=40, overlap=8)):
        KB_CHUNKS.append({
            "doc_id": doc["id"],
            "title": doc["title"],
            "chunk_id": f"{doc['id']}#chunk{i}",
            "text": ch
        })

# 3. Retriever (TF-IDF)
corpus = [c["text"] for c in KB_CHUNKS]
vectorizer = TfidfVectorizer(stop_words="english")
chunk_matrix = vectorizer.fit_transform(corpus)

def retrieve(query: str, k: int = 3) -> List[Dict]:
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, chunk_matrix)[0]
    top_idx = np.argsort(-sims)[:k]
    results = []
    for rank, idx in enumerate(top_idx, start=1):
        item = KB_CHUNKS[idx].copy()
        item["score"] = float(sims[idx])
        item["rank"] = rank
        results.append(item)
    return results

# 4. Generation (Hugging Face)
GENERATION_MODEL = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(GENERATION_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(
    GENERATION_MODEL,
    device_map="auto",
)

def gen(prompt, max_new_tokens=200):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return [{"generated_text": tokenizer.decode(outputs[0], skip_special_tokens=True)}]

SYSTEM_MSG = (
    "You are a helpful assistant. Use ONLY the context to answer the question. "
    "Cite sources inline as [source: <chunk_id>]. If the answer is not in the context, say you don't know."
)

def build_prompt(query: str, retrieved: List[Dict]) -> str:
    context_blocks = []
    for r in retrieved:
        context_blocks.append(f"[{r['chunk_id']}] (title: {r['title']})\n{r['text']}")
    context_text = "\n\n".join(context_blocks)
    prompt = (
        f"{SYSTEM_MSG}\n\n"
        f"### Context\n{context_text}\n\n"
        f"### Question\n{query}\n\n"
        f"### Answer"
    )
    return prompt

def rag_answer(query: str, k: int = 3) -> Dict:
    top = retrieve(query, k=k)
    prompt = build_prompt(query, top)
    out = gen(prompt, max_new_tokens=200)[0]["generated_text"]
    return {"answer": out, "retrieved": top, "prompt": prompt}

def show_result(result: Dict):
    print("\nANSWER:\n")
    print(result["answer"])
    print("\nCITATIONS:")
    for r in result["retrieved"]:
        print(f"  - {r['rank']}. {r['title']} [{r['chunk_id']}]  (score={r['score']:.3f})")

if __name__ == "__main__":
    user_query = "Why is chunking useful in RAG?"
    print(f"User Query: {user_query}")
    result = rag_answer(user_query, k=3)
    show_result(result)
