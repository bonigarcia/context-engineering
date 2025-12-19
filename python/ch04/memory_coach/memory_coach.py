#!/usr/bin/env python3
"""
Memory Coach: a CLI AI assistant that demonstrates practical memory management.

Key ideas:
- Short-term memory: sliding window + rolling summary
- Long-term memory:
  * Semantic memory: user profile stored as key/value in SQLite
  * Episodic memory: "memories" stored as embedded snippets in a FAISS index
- Memory policy: the agent decides what to store using an explicit extraction step
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import textwrap
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

import numpy as np
import faiss  # type: ignore
from sentence_transformers import SentenceTransformer  # type: ignore


# -----------------------------
# Models for structured outputs
# -----------------------------

class MemoryWriteDecision(BaseModel):
    """What to store and how."""
    profile_updates: Dict[str, str] = Field(default_factory=dict)
    memories: List[str] = Field(default_factory=list)
    rationale: Optional[str] = None


# -----------------------------
# Storage: SQLite (profile) + FAISS (episodic)
# -----------------------------

class ProfileStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init()

    def _init(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS profile (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def upsert(self, updates: Dict[str, str]) -> None:
        if not updates:
            return
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            for k, v in updates.items():
                conn.execute("""
                    INSERT INTO profile(key, value, updated_at)
                    VALUES(?, ?, ?)
                    ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
                """, (k, v, now))
            conn.commit()

    def get_all(self) -> Dict[str, str]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT key, value FROM profile ORDER BY key").fetchall()
        return {k: v for k, v in rows}

    def clear(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM profile")
            conn.commit()


class EpisodicStore:
    """
    Stores memory snippets with embeddings in a FAISS index.
    We keep a parallel SQLite table to map vector IDs -> text + metadata.
    """
    def __init__(self, db_path: str, index_path: str, embedder: SentenceTransformer):
        self.db_path = db_path
        self.index_path = index_path
        self.embedder = embedder
        self.dim = self._embedding_dim()
        self.index = self._load_or_create_index()
        self._init_db()

    def _embedding_dim(self) -> int:
        test = self.embedder.encode(["test"], normalize_embeddings=True)
        return int(test.shape[1])

    def _load_or_create_index(self) -> faiss.Index:
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        # Cosine similarity via inner product on normalized vectors
        index = faiss.IndexFlatIP(self.dim)
        return index

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS episodic (
                    id INTEGER PRIMARY KEY,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def _next_id(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM episodic").fetchone()
        return int(row[0])

    def add_many(self, memories: List[str]) -> int:
        if not memories:
            return 0

        now = datetime.utcnow().isoformat()
        ids: List[int] = []
        texts: List[str] = []
        with sqlite3.connect(self.db_path) as conn:
            for mem in memories:
                mem = mem.strip()
                if not mem:
                    continue
                mem_id = self._next_id()
                conn.execute("INSERT INTO episodic(id, text, created_at) VALUES(?, ?, ?)", (mem_id, mem, now))
                ids.append(mem_id)
                texts.append(mem)
            conn.commit()

        if not ids:
            return 0

        vecs = self.embedder.encode(texts, normalize_embeddings=True).astype("float32")
        self.index.add_with_ids(vecs, np.array(ids, dtype=np.int64))
        faiss.write_index(self.index, self.index_path)
        return len(ids)

    def search(self, query: str, k: int = 5) -> List[Tuple[int, float, str]]:
        if self.index.ntotal == 0:
            return []
        q = self.embedder.encode([query], normalize_embeddings=True).astype("float32")
        scores, ids = self.index.search(q, k)
        results: List[Tuple[int, float, str]] = []
        for mem_id, score in zip(ids[0].tolist(), scores[0].tolist()):
            if mem_id == -1:
                continue
            text = self._get_text(mem_id)
            if text:
                results.append((int(mem_id), float(score), text))
        return results

    def _get_text(self, mem_id: int) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT text FROM episodic WHERE id=?", (mem_id,)).fetchone()
        return row[0] if row else None

    def list_recent(self, limit: int = 10) -> List[Tuple[int, str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT id, created_at, text FROM episodic ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [(int(r[0]), str(r[1]), str(r[2])) for r in rows]

    def clear(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM episodic")
            conn.commit()
        self.index = faiss.IndexFlatIP(self.dim)
        faiss.write_index(self.index, self.index_path)


# -----------------------------
# Short-term memory: window + summary
# -----------------------------

@dataclass
class ShortTermMemory:
    max_turns: int = 10
    summarize_every: int = 6
    messages: List[Dict[str, str]] = None
    summary: str = ""

    def __post_init__(self) -> None:
        if self.messages is None:
            self.messages = []

    def add_user(self, text: str) -> None:
        self.messages.append({"role": "user", "content": text})
        self._trim()

    def add_assistant(self, text: str) -> None:
        self.messages.append({"role": "assistant", "content": text})
        self._trim()

    def _trim(self) -> None:
        # Keep the last max_turns*2 messages (user+assistant turns)
        max_msgs = self.max_turns * 2
        if len(self.messages) > max_msgs:
            self.messages = self.messages[-max_msgs:]

    def should_summarize(self) -> bool:
        # Trigger periodically based on number of messages since last summary refresh.
        return len(self.messages) >= self.summarize_every * 2


# -----------------------------
# LLM wrapper
# -----------------------------

class LLM:
    def __init__(self, model: str):
        self.client = OpenAI()
        self.model = model

    def chat(self, system: str, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}] + messages,
            temperature=temperature,
        )
        return resp.choices[0].message.content or ""

    def extract_memory(self, system: str, messages: List[Dict[str, str]]) -> MemoryWriteDecision:
        """
        Ask the model to decide what should be written to long-term memory.
        Returns a validated JSON object.
        """
        extraction_prompt = system + "\n\n" + textwrap.dedent("""\
        You are a memory extraction component.
        Return ONLY valid JSON matching this schema:
        {
          "profile_updates": { "key": "value", ... },
          "memories": ["short memory sentence", ...],
          "rationale": "optional short rationale"
        }

        Rules:
        - Profile updates must be stable user preferences or facts likely to remain true.
        - Memories should be episodic: helpful events, decisions, constraints, or outcomes.
        - Avoid storing sensitive data (passwords, secrets, financial identifiers).
        - If nothing should be stored, return empty profile_updates and memories.
        """).strip()

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": extraction_prompt}] + messages,
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        raw = resp.choices[0].message.content or "{}"
        try:
            data = json.loads(raw)
            return MemoryWriteDecision.model_validate(data)
        except (json.JSONDecodeError, ValidationError):
            # Conservative fallback: store nothing
            return MemoryWriteDecision(profile_updates={}, memories=[], rationale="Invalid JSON from model; skipped.")


# -----------------------------
# Prompt building
# -----------------------------

def render_profile(profile: Dict[str, str]) -> str:
    if not profile:
        return "No stored user profile yet."
    lines = [f"- {k}: {v}" for k, v in profile.items()]
    return "\n".join(lines)

def render_retrieved(memories: List[Tuple[int, float, str]]) -> str:
    if not memories:
        return "None."
    lines = []
    for mem_id, score, text in memories:
        lines.append(f"- (id={mem_id}, score={score:.3f}) {text}")
    return "\n".join(lines)


def build_system_prompt(profile: Dict[str, str], retrieved: List[Tuple[int, float, str]], summary: str) -> str:
    return textwrap.dedent(f"""\
    You are Memory Coach, a practical assistant that helps the user plan and reflect.

    Operate with these constraints:
    - Prefer asking one clarifying question if required.
    - Be concise but actionable.
    - Do not invent personal facts; rely on provided context, profile, and retrieved memories.

    USER PROFILE (semantic long-term memory)
    {render_profile(profile)}

    RETRIEVED MEMORIES (episodic long-term memory; may be partial or outdated)
    {render_retrieved(retrieved)}

    RUNNING SUMMARY (compressed short-term memory)
    {summary if summary.strip() else "No summary yet."}
    """).strip()


def build_summarization_prompt() -> str:
    return textwrap.dedent("""\
    You are a summarization component for an assistant.
    Produce an updated running summary of the conversation so far.

    Requirements:
    - Keep it under 1200 characters.
    - Capture user goals, constraints, preferences stated in-session, and decisions made.
    - Do not include chit-chat.
    - Use neutral language; avoid assumptions.
    """).strip()


# -----------------------------
# CLI commands
# -----------------------------

HELP_TEXT = """\
Commands:
/help                 Show this help
/profile              Show stored user profile (semantic memory)
/memories             Show most recent episodic memories
/forget               Clear all long-term memory (profile + episodic)
/reset                Clear short-term context (window + summary)
/exit                 Quit
"""

def is_command(text: str) -> bool:
    return text.strip().startswith("/")

# -----------------------------
# Main REPL
# -----------------------------

def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Memory Coach (hands-on memory management demo)")
    parser.add_argument("--model", default=os.getenv("MODEL", "gpt-4.1-mini"), help="Chat model name")
    parser.add_argument("--data-dir", default=os.getenv("DATA_DIR", ".memory_coach"), help="Directory for memory data")
    parser.add_argument("--max-turns", type=int, default=10, help="Short-term sliding window turns")
    parser.add_argument("--summarize-every", type=int, default=6, help="Summarize after this many turns")
    parser.add_argument("--top-k", type=int, default=5, help="Top-K episodic memories to retrieve")
    args = parser.parse_args()

    console = Console()

    data_dir = os.path.abspath(args.data_dir)
    os.makedirs(data_dir, exist_ok=True)
    profile_db = os.path.join(data_dir, "profile.sqlite")
    episodic_db = os.path.join(data_dir, "episodic.sqlite")
    faiss_index = os.path.join(data_dir, "episodic.index")

    embedder_name = os.getenv("EMBEDDER", "sentence-transformers/all-MiniLM-L6-v2")
    console.print(f"[bold]Memory Coach[/bold] using model={args.model} embedder={embedder_name}")
    console.print("Type /help for commands.\n")

    embedder = SentenceTransformer(embedder_name)
    profile_store = ProfileStore(profile_db)
    episodic_store = EpisodicStore(episodic_db, faiss_index, embedder)
    stm = ShortTermMemory(max_turns=args.max_turns, summarize_every=args.summarize_every)

    llm = LLM(args.model)

    while True:
        try:
            user_text = Prompt.ask("[bold cyan]you[/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nExiting.")
            return 0

        if not user_text:
            continue

        if is_command(user_text):
            cmd = user_text.strip().lower()
            if cmd == "/help":
                console.print(HELP_TEXT)
            elif cmd == "/profile":
                prof = profile_store.get_all()
                console.print("[bold]User profile[/bold]")
                console.print(render_profile(prof) + "\n")
            elif cmd == "/memories":
                rows = episodic_store.list_recent(limit=10)
                console.print("[bold]Recent episodic memories[/bold]")
                if not rows:
                    console.print("None.\n")
                else:
                    for mem_id, created_at, text in rows:
                        console.print(f"- (id={mem_id}, {created_at}) {text}")
                    console.print()
            elif cmd == "/forget":
                profile_store.clear()
                episodic_store.clear()
                console.print("Cleared long-term memory (profile + episodic).\n")
            elif cmd == "/reset":
                stm.messages = []
                stm.summary = ""
                console.print("Cleared short-term context (window + summary).\n")
            elif cmd == "/exit":
                console.print("Goodbye.")
                return 0
            else:
                console.print("Unknown command. Type /help.\n")
            continue

        # 1) Add user message to short-term memory
        stm.add_user(user_text)

        # 2) Retrieve long-term memories relevant to the new message
        retrieved = episodic_store.search(user_text, k=args.top_k)
        profile = profile_store.get_all()

        # 3) Optionally update running summary (compression)
        if stm.should_summarize():
            sum_system = build_summarization_prompt()
            # Provide current summary + recent window as input
            sum_messages = []
            if stm.summary.strip():
                sum_messages.append({"role": "user", "content": f"Current summary:\n{stm.summary}"})
            window_text = "\n".join([f"{m['role']}: {m['content']}" for m in stm.messages])
            sum_messages.append({"role": "user", "content": f"Conversation window:\n{window_text}"})
            new_summary = llm.chat(sum_system, sum_messages, temperature=0.0)
            stm.summary = new_summary.strip()

        # 4) Build system prompt with profile + retrieved memories + summary
        system = build_system_prompt(profile, retrieved, stm.summary)

        # 5) Ask the model to respond
        assistant_text = llm.chat(system, stm.messages, temperature=0.2).strip()
        stm.add_assistant(assistant_text)
        console.print(Markdown(assistant_text))
        console.print()

        # 6) Decide what to store (memory write policy)
        decision_system = textwrap.dedent("""\
        You are Memory Coach. Decide what should be written to long-term memory from the latest interaction.
        """).strip()
        decision_messages = [
            {"role": "user", "content": f"Latest user message:\n{user_text}"},
            {"role": "assistant", "content": assistant_text},
        ]
        decision = llm.extract_memory(decision_system, decision_messages)

        # 7) Persist semantic + episodic memories
        profile_store.upsert(decision.profile_updates)
        episodic_store.add_many(decision.memories)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
