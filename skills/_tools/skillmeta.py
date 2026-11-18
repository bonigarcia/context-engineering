"""Read Agent Skills frontmatter for the repo tooling (catalog and evals).

Skills never import this module. Each skill stays installable on its own.
"""

from pathlib import Path

SKIPPED_DIRS = {"evals"}


class FrontmatterError(ValueError):
    """Raised when a SKILL.md frontmatter block is missing or unsupported."""


def _unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _split_key(line, number):
    if ":" not in line:
        raise FrontmatterError(f"line {number}: expected 'key: value'")
    key, value = line.split(":", 1)
    key = key.strip()
    if not key:
        raise FrontmatterError(f"line {number}: empty key")
    return key, value.strip()


def parse_frontmatter(text):
    """Return (frontmatter dict, body) for a SKILL.md text.

    Supports 'key: value' lines, quoted values, and one nested level of
    'key: value' lines under 'metadata:'. Anything else raises FrontmatterError.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("missing opening '---' fence")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise FrontmatterError("missing closing '---' fence") from None

    data = {}
    current_map = None
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if current_map is None:
                raise FrontmatterError(f"line {number}: unexpected indentation")
            stripped = line.strip()
            if stripped.startswith("- "):
                raise FrontmatterError(f"line {number}: lists are not supported")
            key, value = _split_key(stripped, number)
            if not value:
                raise FrontmatterError(f"line {number}: nesting deeper than one level")
            current_map[key] = _unquote(value)
            continue
        key, value = _split_key(line, number)
        if value:
            if value[0] in "[{|>":
                raise FrontmatterError(f"line {number}: unsupported value syntax")
            data[key] = _unquote(value)
            current_map = None
        else:
            current_map = {}
            data[key] = current_map
    return data, "\n".join(lines[end + 1:])


def _chapter_key(skill):
    chapter = skill["metadata"].get("chapter", "")
    return (int(chapter) if chapter.isdigit() else 99, skill["name"])


def load_skills(root):
    """Load every root/*/SKILL.md, skipping tooling folders, sorted by chapter."""
    root = Path(root)
    skills = []
    for skill_file in sorted(root.glob("*/SKILL.md")):
        dirname = skill_file.parent.name
        if dirname.startswith("_") or dirname in SKIPPED_DIRS:
            continue
        data, body = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        metadata = data.get("metadata")
        skills.append(
            {
                "name": data.get("name", dirname),
                "description": data.get("description", ""),
                "metadata": metadata if isinstance(metadata, dict) else {},
                "path": f"skills/{dirname}",
                "body": body,
            }
        )
    return sorted(skills, key=_chapter_key)
