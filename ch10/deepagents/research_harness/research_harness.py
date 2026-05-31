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

from pathlib import Path
from typing import Iterable

try:
    from deepagents import create_deep_agent
except ImportError:  # pragma: no cover - lets tests monkeypatch the builder
    create_deep_agent = None


RESEARCH_TASK = (
    "Research how this repository organizes the DeepAgents examples and write a concise brief "
    "using bounded notes."
)
SYSTEM_PROMPT = (
    "You are a concise research assistant. Inspect repo and docs markdown, keep notes bounded, "
    "and return a short, useful brief."
)


def list_markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def read_markdown_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def _resolve_markdown_path(repo_root: Path, relative_path: str) -> Path:
    path = (repo_root / relative_path).resolve()
    if path.suffix.lower() != ".md":
        raise ValueError("Only markdown files are allowed")
    if repo_root.resolve() not in path.parents and path != repo_root.resolve():
        raise ValueError("Path must stay inside the repository root")
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def summarize_bounded_notes(notes: Iterable[str], limit: int = 5) -> str:
    bounded = [note.strip() for note in list(notes)[-limit:] if note.strip()]
    if not bounded:
        return "(no notes)"
    return "\n".join(f"- {note.splitlines()[0]}" for note in bounded)


def _tool(name: str, description: str):
    def decorator(func):
        func.name = name
        func.description = description
        return func

    return decorator


def build_agent(root: Path | None = None):
    if create_deep_agent is None:
        raise RuntimeError("deepagents.create_deep_agent is not available")

    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[3]

    @_tool("list_markdown_files", "List markdown files available for repository and docs research.")
    def list_markdown_files_tool() -> str:
        return "\n".join(path.relative_to(repo_root).as_posix() for path in list_markdown_files(repo_root))

    @_tool("read_markdown_file", "Read a markdown file relative to the repository root.")
    def read_markdown_file_tool(path: str) -> str:
        return read_markdown_file(_resolve_markdown_path(repo_root, path))

    @_tool("summarize_bounded_notes", "Summarize newline-separated notes while keeping only a bounded tail.")
    def summarize_bounded_notes_tool(notes: str, limit: int = 5) -> str:
        return summarize_bounded_notes(notes.splitlines(), limit=limit)

    return create_deep_agent(
        model="openai:gpt-5.4",
        system_prompt=SYSTEM_PROMPT,
        tools=[list_markdown_files_tool, read_markdown_file_tool, summarize_bounded_notes_tool],
    )


def main() -> None:
    agent = build_agent()
    result = agent.invoke({"messages": [("user", RESEARCH_TASK)]})
    print(result)


if __name__ == "__main__":
    main()
