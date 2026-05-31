from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def select_files(root: Path) -> list[Path]:
    return [
        root / "README.md",
        root / "file_context" / "README.md",
        root / "planning_loop" / "README.md",
    ]


def summarize_file(path: Path) -> str:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines[0].lstrip("# ") if lines else path.name


def merge_notes(notes: list[str]) -> dict[str, object]:
    return {"context_state": notes[:2], "note_count": len(notes)}


def write_brief(context_state: dict[str, object]) -> str:
    notes = context_state["context_state"]
    return "\n".join([
        "# Subagent delegation",
        "",
        "Delegated steps:",
        "- select files",
        "- summarize files",
        "- merge notes",
        "- write brief",
        "",
        f"Merged {context_state['note_count']} notes into context_state.",
        *[f"- {note}" for note in notes],
    ])


def main() -> None:
    root = repo_root() / "ch10" / "deepagents"
    files = select_files(root)
    notes = [summarize_file(path) for path in files]
    context_state = merge_notes(notes)
    print(write_brief(context_state))


if __name__ == "__main__":
    main()
