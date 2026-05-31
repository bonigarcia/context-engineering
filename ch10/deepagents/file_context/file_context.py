from __future__ import annotations

from collections import deque
from pathlib import Path


BUFFER_LIMIT = 3


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def trim_note(path: Path) -> str:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    heading = lines[0].lstrip("# ") if lines else path.name
    detail = next((line[2:] for line in lines[1:] if line.startswith("- ")), lines[1] if len(lines) > 1 else "")
    note = f"{heading}: {detail}".strip()
    return note[:100]


def main() -> None:
    root = repo_root() / "ch10" / "deepagents"
    sources = [
        root / "README.md",
        root / "research_harness" / "README.md",
        root / "subagent_delegation" / "README.md",
        root / "planning_loop" / "README.md",
        root / "human_approval" / "README.md",
    ]

    notes = deque(maxlen=BUFFER_LIMIT)
    for source in sources:
        notes.append((source.relative_to(root).as_posix(), trim_note(source)))

    print("# File context")
    print(f"Bounded note buffer: {BUFFER_LIMIT}")
    print("Trimmed notes:")
    for source, note in notes:
        print(f"- {source}: {note}")


if __name__ == "__main__":
    main()
