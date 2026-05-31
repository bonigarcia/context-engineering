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

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Deque


TASK = (
    "Research how this repository organizes chapter 10 orchestration examples "
    "and explain how the DeepAgents slice manages context."
)
NOTE_LIMIT = 5
FILE_LIMIT = 5
SNIPPET_LIMIT = 1200
STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "this",
    "that",
    "from",
    "into",
    "about",
    "using",
    "example",
    "examples",
    "readme",
    "chapter",
    "context",
    "task",
    "run",
    "small",
    "local",
}


@dataclass(frozen=True)
class Note:
    source: str
    summary: str


class LocalFileTool:
    def __init__(self, root: Path) -> None:
        self.root = root

    def list_sources(self) -> list[Path]:
        candidates = [
            self.root / "README.md",
            self.root / "docs" / "README.md",
            self.root / "docs" / "superpowers" / "plans" / "2026-05-31-ch10-orchestration-frameworks-phase1.md",
            self.root / "ch10" / "README.md",
            self.root / "ch10" / "langgraph" / "README.md",
            self.root / "ch10" / "crewai" / "research_and_write" / "README.md",
            self.root / "ch10" / "agent_framework" / "basic_conversation" / "README.md",
        ]

        discovered = sorted(
            path
            for path in self.root.glob("ch10/**/*.md")
            if path.is_file() and "__pycache__" not in path.parts
        )
        candidates.extend(discovered)

        selected: list[Path] = []
        seen: set[Path] = set()
        for path in candidates:
            if path in seen or not path.exists() or not path.is_file():
                continue
            selected.append(path)
            seen.add(path)
            if len(selected) >= FILE_LIMIT:
                break
        return selected

    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")[:SNIPPET_LIMIT]


class BoundedNoteBuffer:
    def __init__(self, limit: int) -> None:
        self._items: Deque[Note] = deque(maxlen=limit)

    def add(self, note: Note) -> None:
        self._items.append(note)

    def items(self) -> list[Note]:
        return list(self._items)


def find_repo_root(start: Path) -> Path:
    for candidate in start.parents:
        if (candidate / "README.md").exists() and (candidate / "ch10").exists():
            return candidate
    raise RuntimeError("Could not locate the repository root")


def normalize_words(text: str) -> list[str]:
    words = []
    for raw in text.replace("/", " ").replace("-", " ").split():
        cleaned = "".join(char for char in raw.lower() if char.isalnum())
        if len(cleaned) < 4 or cleaned in STOPWORDS:
            continue
        words.append(cleaned)
    return words


def summarize_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    headings = [line.lstrip("# ") for line in lines if line.startswith("#")][:2]
    bullets = [line for line in lines if line.startswith("-")][:2]
    if headings and bullets:
        return f"{headings[0]} | {'; '.join(bullets)}"
    if headings:
        return f"{headings[0]} | {lines[1] if len(lines) > 1 else ''}".strip(" |")
    return lines[0] if lines else "(empty file)"


def collect_notes(tool: LocalFileTool) -> BoundedNoteBuffer:
    buffer = BoundedNoteBuffer(NOTE_LIMIT)
    for source in tool.list_sources():
        content = tool.read(source)
        buffer.add(Note(source=source.relative_to(tool.root).as_posix(), summary=summarize_text(content)))
    return buffer


def reduce_context(task: str, notes: BoundedNoteBuffer) -> dict[str, object]:
    note_items = notes.items()
    keyword_counter: Counter[str] = Counter()
    for note in note_items:
        keyword_counter.update(normalize_words(note.summary))

    context_state = {
        "task": task,
        "buffer_limit": NOTE_LIMIT,
        "note_count": len(note_items),
        "sources": [note.source for note in note_items],
        "note_summaries": [note.summary for note in note_items],
        "signals": [word for word, _ in keyword_counter.most_common(4)],
    }
    return context_state


def synthesize_brief(context_state: dict[str, object]) -> str:
    sources = context_state["sources"]
    notes = context_state["note_summaries"]
    signals = context_state["signals"]

    lines = [
        "# Research brief",
        "",
        f"Task: {context_state['task']}",
        "",
        "## Context state",
        f"- Bounded note buffer: {context_state['buffer_limit']}",
        f"- Notes kept: {context_state['note_count']}",
        "",
        "## What I inspected",
    ]
    lines.extend(f"- {source}" for source in sources)
    lines.extend([
        "",
        "## Context signals",
    ])
    if signals:
        lines.extend(f"- {signal}" for signal in signals)
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Reduced notes",
    ])
    lines.extend(f"- {note}" for note in notes)
    lines.extend([
        "",
        "## Conclusion",
        "- The harness keeps only a bounded note buffer, compresses those notes into a reduced context state, and uses that state for the final brief.",
        "- This keeps the example focused on long-horizon repo/docs research without carrying the full file text forward.",
    ])
    return "\n".join(lines)


def main() -> None:
    root = find_repo_root(Path(__file__).resolve())
    tool = LocalFileTool(root)
    notes = collect_notes(tool)
    context_state = reduce_context(TASK, notes)
    print(synthesize_brief(context_state))


if __name__ == "__main__":
    main()
