#!/usr/bin/env python3
"""Generate docs/skills.json from the frontmatter of every skill.

Usage (from the repo root): python3 skills/_tools/build_catalog.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from skillmeta import load_skills  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
FIELDS = {"chapter": "chapter", "chapterTitle": "chapter-title", "input": "input", "output": "output"}


def build_catalog(root):
    catalog = []
    for skill in load_skills(root):
        metadata = skill["metadata"]
        missing = [key for key in FIELDS.values() if not metadata.get(key)]
        if missing:
            print(f"warning: {skill['name']} has no metadata for {', '.join(missing)}", file=sys.stderr)
        entry = {"name": skill["name"], "description": skill["description"]}
        entry.update({field: metadata.get(key, "") for field, key in FIELDS.items()})
        entry["path"] = skill["path"]
        catalog.append(entry)
    return catalog


def write_catalog(root, out):
    catalog = build_catalog(root)
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    Path(out).write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
    return len(catalog)


def main():
    out = REPO_ROOT / "docs" / "skills.json"
    count = write_catalog(REPO_ROOT / "skills", out)
    print(f"{count} skills written to {out.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
