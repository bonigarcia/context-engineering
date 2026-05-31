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


def reduce_notes(notes: list[str], limit: int = 2) -> list[str]:
    return notes[-limit:]


def main() -> None:
    root = repo_root() / "ch10" / "deepagents"
    files = select_files(root)
    notes = [summarize_file(path) for path in files]
    reduced = reduce_notes(notes)

    print("# File context")
    print()
    print("Selected files:")
    for path in files:
        print(f"- {path.relative_to(root).as_posix()}")
    print()
    print("Trimmed note buffer:")
    for note in reduced:
        print(f"- {note}")
    print()
    print("Bounded note buffer preserved the useful shape of the repo.")


if __name__ == "__main__":
    main()
