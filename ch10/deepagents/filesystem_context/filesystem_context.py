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

try:
    from deepagents import create_deep_agent
    from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend, StoreBackend
except ImportError:  # pragma: no cover - keeps the example importable without deps
    create_deep_agent = None
    CompositeBackend = None
    FilesystemBackend = None
    StateBackend = None
    StoreBackend = None

try:
    from langgraph.store.memory import InMemoryStore
except ImportError:  # pragma: no cover - keeps the example importable without deps
    InMemoryStore = None


MEMORIES_PATH = "/memories/AGENTS.md"
WORKSPACE_NOTES_PATH = "/workspace/notes.md"
MEMORIES_CONTENT = "# AGENTS.md\n- Keep agent context explicit.\n"
WORKSPACE_CONTENT = "# Notes\n- Filesystem-backed context is visible.\n"

_MEMORY_ROOT = Path(__file__).resolve().with_name("memory")
_WORKSPACE_ROOT = Path(__file__).resolve().with_name("workspace")
_BACKEND = None
_STORE = None


def _namespace(_runtime):
    return ("filesystem_context", "memories")


def _seed_workspace_notes() -> Path:
    _WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
    notes_path = _WORKSPACE_ROOT / "notes.md"
    if not notes_path.exists():
        notes_path.write_text(WORKSPACE_CONTENT, encoding="utf-8")
    return _WORKSPACE_ROOT


def _seed_memory_file() -> Path:
    _MEMORY_ROOT.mkdir(parents=True, exist_ok=True)
    memory_path = _MEMORY_ROOT / "AGENTS.md"
    if not memory_path.exists():
        memory_path.write_text(MEMORIES_CONTENT, encoding="utf-8")
    return _MEMORY_ROOT


def build_store():
    if InMemoryStore is None:
        raise RuntimeError("langgraph.store.memory.InMemoryStore is unavailable; install ../requirements.txt")

    global _STORE
    if _STORE is None:
        store = InMemoryStore()
        store.put(_namespace(None), "AGENTS.md", {"content": MEMORIES_CONTENT})
        _STORE = store
    return _STORE


def build_backend():
    if None in (CompositeBackend, FilesystemBackend, StateBackend, StoreBackend):
        raise RuntimeError("deepagents filesystem backends are unavailable; install ../requirements.txt")

    global _BACKEND
    if _BACKEND is None:
        _seed_memory_file()
        _seed_workspace_notes()
        _BACKEND = CompositeBackend(
            default=StateBackend(),
            routes={
                "/memories/": FilesystemBackend(root_dir=str(_MEMORY_ROOT), virtual_mode=True),
                "/workspace/": FilesystemBackend(root_dir=str(_WORKSPACE_ROOT), virtual_mode=True),
            },
        )
    return _BACKEND


def build_agent():
    if create_deep_agent is None:
        raise RuntimeError("deepagents.create_deep_agent is unavailable; install ../requirements.txt")

    return create_deep_agent(
        model="openai:gpt-5.4",
        memory=[MEMORIES_PATH],
        backend=build_backend(),
        store=build_store(),
        tools=[],
        system_prompt=(
            "You are a DeepAgents filesystem-context demo. "
            "Route context through filesystem-like paths instead of hidden state."
        ),
    )


def main() -> None:
    build_agent()
    print(f"Seeded {MEMORIES_PATH} and {WORKSPACE_NOTES_PATH}.")


if __name__ == "__main__":
    main()
