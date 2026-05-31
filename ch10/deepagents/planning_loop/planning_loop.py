from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def select_files(root: Path) -> list[Path]:
    return [
        root / "README.md",
        root / "research_harness" / "README.md",
        root / "file_context" / "README.md",
    ]


def summarize_file(path: Path) -> str:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines[0].lstrip("# ") if lines else path.name


def reduce_context(notes: list[str]) -> dict[str, object]:
    return {"context_state": notes[-2:], "note_count": len(notes)}


def main() -> None:
    root = repo_root() / "ch10" / "deepagents"
    print("# Planning loop")
    print()

    all_notes: list[str] = []
    for index, path in enumerate(select_files(root), start=1):
        note = summarize_file(path)
        all_notes.append(note)
        print(f"Pass {index}: {path.name}")
        print(f"- note: {note}")

    reduced = reduce_context(all_notes)
    print()
    print("Reduced context:")
    for note in reduced["context_state"]:
        print(f"- {note}")
    print(f"- reduced from {reduced['note_count']} passes")


if __name__ == "__main__":
    main()
