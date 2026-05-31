from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def main() -> None:
    root = repo_root() / "ch10" / "deepagents"
    files = [
        root / "README.md",
        root / "research_harness" / "README.md",
        root / "file_context" / "README.md",
    ]

    print("# Planning loop")
    print("Pass 1: select a small file set")
    print(f"Pass 2: reduced context from {len(files)} files into a narrow summary")
    print("Pass 3: reduced context becomes the final brief")


if __name__ == "__main__":
    main()
