import os
import hashlib
import json
import re
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Set, Tuple

from dotenv import load_dotenv
from openai import OpenAI

import chromadb
from chromadb.config import Settings


RUN_LOG_PATH = "ragops_runs.jsonl"
CHROMA_DIR = "chroma_store"
COLLECTION_NAME = "basic_ragops_docs"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_id: str
    text: str


_CITATION_RE = re.compile(r"\[(\d+)\]")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_run_event(event: Dict[str, Any], log_path: str = RUN_LOG_PATH) -> None:
    event = dict(event)
    event.setdefault("ts_utc", utc_now_iso())
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def stable_chunk_id(source_id: str, chunk_text: str) -> str:
    digest = hashlib.sha256((source_id + "\n" + chunk_text).encode("utf-8")).hexdigest()
    return digest[:32]


def simple_chunk_text(text: str, source_id: str, max_chars: int = 700, overlap_chars: int = 120) -> List[Chunk]:
    normalized = " ".join(text.split())
    chunks: List[Chunk] = []
    start = 0
    while start < len(normalized):
        end = min(len(normalized), start + max_chars)
        chunk_text = normalized[start:end].strip()
        if chunk_text:
            chunks.append(
                Chunk(
                    chunk_id=stable_chunk_id(source_id, chunk_text),
                    source_id=source_id,
                    text=chunk_text,
                )
            )
        if end >= len(normalized):
            break
        start = max(0, end - overlap_chars)
    return chunks


def build_corpus() -> List[Tuple[str, str]]:
    docs: List[Tuple[str, str]] = []

    docs.append(
        (
            "policy_remote_work",
            """
Remote work policy

Employees can work remotely up to three days per week.
Core collaboration hours are 10:00 to 16:00 in the local time zone of the team.
Requests for exceptions require manager approval.
Company devices must be used for customer data, and local storage is not permitted.
""",
        )
    )

    docs.append(
        (
            "policy_travel",
            """
Travel policy

Domestic flights must be economy class.
International flights longer than six hours can be premium economy.
Meal reimbursement requires an itemized receipt.
Personal travel extensions are allowed if the incremental cost is paid by the employee.
""",
        )
    )

    docs.append(
        (
            "product_overview",
            """
Product overview

Acme Assist is a support automation service that drafts replies for human agents.
It uses retrieval augmented generation with an internal knowledge base.
The system provides citations that point to the source snippets used to craft the answer.
The product supports weekly index refresh and continuous monitoring of retrieval quality.
""",
        )
    )

    return docs


def create_openai_client() -> OpenAI:
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Set it in the environment or a .env file.")
    return OpenAI(api_key=api_key)


def get_chroma_client() -> chromadb.PersistentClient:
    settings = Settings(anonymized_telemetry=False)
    return chromadb.PersistentClient(path=CHROMA_DIR, settings=settings)


def embed_texts(client: OpenAI, texts: List[str]) -> List[List[float]]:
    t0 = time.time()
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    vectors = [d.embedding for d in resp.data]
    write_run_event(
        {
            "event": "embeddings_created",
            "model": EMBEDDING_MODEL,
            "count": len(texts),
            "latency_ms": int((time.time() - t0) * 1000),
        }
    )
    return vectors


def ensure_index(client: OpenAI) -> None:
    corpus = build_corpus()

    all_chunks: List[Chunk] = []
    for source_id, doc_text in corpus:
        all_chunks.extend(simple_chunk_text(doc_text, source_id=source_id))

    write_run_event(
        {
            "event": "ingestion_prepared",
            "sources": len(corpus),
            "chunks": len(all_chunks),
            "chunking": {"max_chars": 700, "overlap_chars": 120},
        }
    )

    chroma_client = get_chroma_client()
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    existing = set(collection.get().get("ids", []))
    new_chunks = [c for c in all_chunks if c.chunk_id not in existing]

    if not new_chunks:
        write_run_event({"event": "index_up_to_date", "collection": COLLECTION_NAME, "chroma_dir": CHROMA_DIR})
        return

    texts = [c.text for c in new_chunks]
    vectors = embed_texts(client, texts)

    ids = [c.chunk_id for c in new_chunks]
    metadatas = [{"source_id": c.source_id} for c in new_chunks]

    t0 = time.time()
    collection.add(ids=ids, documents=texts, embeddings=vectors, metadatas=metadatas)
    write_run_event(
        {
            "event": "index_updated",
            "collection": COLLECTION_NAME,
            "added_chunks": len(new_chunks),
            "latency_ms": int((time.time() - t0) * 1000),
        }
    )


def retrieve_context(client: OpenAI, query: str, k: int = 4) -> List[Dict[str, Any]]:
    chroma_client = get_chroma_client()
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    total = int(collection.count())
    if total <= 0:
        raise RuntimeError("Chroma collection is empty. Indexing should have populated it.")

    k_eff = min(k, total)

    q_vec = embed_texts(client, [query])[0]

    t0 = time.time()
    res = collection.query(
        query_embeddings=[q_vec],
        n_results=k_eff,
        include=["documents", "metadatas", "distances"],
    )
    latency_ms = int((time.time() - t0) * 1000)

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    ids = res.get("ids", [[]])[0]

    snippets: List[Dict[str, Any]] = []
    for i in range(len(docs)):
        snippets.append(
            {
                "cite": i + 1,
                "chunk_id": ids[i],
                "source_id": metas[i].get("source_id", "unknown"),
                "distance": dists[i],
                "text": docs[i],
            }
        )

    write_run_event(
        {
            "event": "retrieval_completed",
            "query": query,
            "k_requested": k,
            "k_used": k_eff,
            "collection_count": total,
            "latency_ms": latency_ms,
            "results": [{"cite": s["cite"], "source_id": s["source_id"], "distance": s["distance"]} for s in snippets],
        }
    )
    return snippets


def build_prompt(query: str, snippets: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    context_lines: List[str] = []
    for s in snippets:
        context_lines.append(f"[{s['cite']}] source_id={s['source_id']} chunk_id={s['chunk_id']}\n{s['text']}\n")

    context_block = "\n".join(context_lines).strip()

    system_msg = (
        "You are a helpful assistant. Use only the provided context to answer. "
        "If the context does not contain the answer, say that the answer is not in the provided context. "
        "Write two to five lines. Each line is a single sentence. Do not use bullet points."
    )

    user_msg = (
        "Context:\n"
        f"{context_block}\n\n"
        "Task:\n"
        f"{query}\n"
    )

    return [{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}]


def extract_citations(text: str) -> Set[int]:
    cites: Set[int] = set()
    for m in _CITATION_RE.finditer(text):
        try:
            cites.add(int(m.group(1)))
        except ValueError:
            pass
    return cites


def enforce_one_citation_per_line(answer: str, snippet_count: int) -> str:
    allowed = list(range(1, snippet_count + 1))
    if not allowed:
        return answer

    default_cite = f"[{allowed[0]}]"

    lines = [ln.strip() for ln in answer.splitlines() if ln.strip()]
    if not lines:
        lines = [answer.strip()] if answer.strip() else []

    fixed: List[str] = []
    for ln in lines:
        ln_clean = _CITATION_RE.sub("", ln).strip()

        # Ensure the line ends with a period before adding citation.
        if ln_clean.endswith((".", "!", "?")):
            ln_clean = ln_clean[:-1].rstrip()

        fixed.append(ln_clean + " " + default_cite + ".")

    return "\n".join(fixed).strip()


def generate_answer(client: OpenAI, query: str, snippets: List[Dict[str, Any]]) -> str:
    messages = build_prompt(query, snippets)

    t0 = time.time()
    resp = client.chat.completions.create(model=CHAT_MODEL, messages=messages, temperature=0.2)
    latency_ms = int((time.time() - t0) * 1000)

    raw = resp.choices[0].message.content.strip()
    normalized = enforce_one_citation_per_line(raw, snippet_count=len(snippets))

    write_run_event(
        {
            "event": "generation_completed",
            "model": CHAT_MODEL,
            "query": query,
            "latency_ms": latency_ms,
            "answer_chars": len(normalized),
        }
    )
    return normalized


def evaluate_answer_format(answer: str, snippet_count: int) -> Dict[str, Any]:
    lines = [ln.strip() for ln in answer.splitlines() if ln.strip()]
    if not lines:
        return {"passed": False, "reason": "empty_answer"}

    allowed = set(range(1, snippet_count + 1))

    lines_with_cite = 0
    invalid_cites: Set[int] = set()

    for ln in lines:
        cites = extract_citations(ln)
        if cites:
            lines_with_cite += 1
        for c in cites:
            if c not in allowed:
                invalid_cites.add(c)

    all_lines_cited = lines_with_cite == len(lines)
    no_invalid = len(invalid_cites) == 0

    return {
        "passed": bool(all_lines_cited and no_invalid),
        "line_count": len(lines),
        "lines_with_citation": lines_with_cite,
        "invalid_citations": sorted(list(invalid_cites)),
    }


def evaluate_regression(client: OpenAI) -> None:
    tests = [
        {"name": "remote_work_days", "query": "How many days per week can employees work remotely?"},
        {"name": "travel_international", "query": "When is premium economy allowed for international flights?"},
        {"name": "product_citations", "query": "What does the product provide to indicate where information came from?"},
    ]

    results: List[Dict[str, Any]] = []

    for tcase in tests:
        query = tcase["query"]
        snippets = retrieve_context(client, query=query, k=4)
        answer = generate_answer(client, query=query, snippets=snippets)

        fmt = evaluate_answer_format(answer, snippet_count=len(snippets))

        results.append(
            {
                "name": tcase["name"],
                "passed": fmt["passed"],
                "line_count": fmt.get("line_count"),
                "lines_with_citation": fmt.get("lines_with_citation"),
                "invalid_citations": fmt.get("invalid_citations"),
            }
        )

    write_run_event({"event": "regression_check_completed", "results": results})

    failures = [r for r in results if not r["passed"]]
    if failures:
        print("Regression check failed")
        for f in failures:
            print(json.dumps(f, ensure_ascii=False))
        raise SystemExit(2)

    print("Regression check passed")


def main() -> None:
    run_id = str(uuid.uuid4())
    write_run_event({"event": "run_started", "run_id": run_id})

    client = create_openai_client()
    ensure_index(client)

    query = "Summarize the remote work policy, including collaboration hours and data handling rules."
    snippets = retrieve_context(client, query=query, k=4)
    answer = generate_answer(client, query=query, snippets=snippets)

    print("Query")
    print(query)
    print()
    print("Answer")
    print(answer)
    print()

    evaluate_regression(client)

    write_run_event({"event": "run_finished", "run_id": run_id})


if __name__ == "__main__":
    main()