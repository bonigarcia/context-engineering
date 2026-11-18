#!/usr/bin/env python3
"""Validate the frontmatter of an Agent Skills directory.

Usage: validate_frontmatter.py SKILL_DIR

Prints OK and exits 0 when the frontmatter is valid. Otherwise prints one
"ERROR: <message>" line per problem and exits 1. Uses PyYAML when it is
installed and a minimal built-in parser otherwise.
"""

import re
import sys
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024


class ParseError(ValueError):
    pass


def split_frontmatter(text):
    lines = text.replace("\r\n", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        raise ParseError("missing opening '---' fence")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index])
    raise ParseError("missing closing '---' fence")


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_minimal(block):
    data = {}
    current = None
    for number, line in enumerate(block.split("\n"), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line.startswith((" ", "\t"))
        stripped = line.strip()
        if stripped.startswith("- ") or ":" not in stripped:
            raise ParseError(f"line {number}: unsupported syntax (lists or multi-line values)")
        key, value = (part.strip() for part in stripped.split(":", 1))
        if indented:
            if current is None or not value:
                raise ParseError(f"line {number}: unsupported nesting")
            current[key] = unquote(value)
        elif value:
            if value[0] in "[{|>":
                raise ParseError(f"line {number}: unsupported value syntax")
            quoted = len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'"
            if not quoted and (": " in value or " #" in value):
                raise ParseError(f"line {number}: value contains ': ' or ' #', quote it")
            data[key] = unquote(value)
            current = None
        else:
            current = {}
            data[key] = current
    return data


def parse(block):
    try:
        import yaml
    except ImportError:
        return parse_minimal(block)
    try:
        data = yaml.safe_load(block) or {}
    except yaml.YAMLError as error:
        raise ParseError(str(error).splitlines()[0]) from None
    if not isinstance(data, dict):
        raise ParseError("frontmatter is not a mapping")
    return data


def validate(skill_dir):
    skill_dir = Path(skill_dir)
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return ["SKILL.md not found"]
    try:
        data = parse(split_frontmatter(skill_file.read_text(encoding="utf-8")))
    except ParseError as error:
        return [f"cannot parse frontmatter: {error}"]

    errors = []
    name = data.get("name")
    if not name:
        errors.append("name is required")
    else:
        name = str(name)
        if len(name) > MAX_NAME:
            errors.append(f"name has {len(name)} characters (max {MAX_NAME})")
        if not NAME_PATTERN.match(name):
            errors.append(
                f"name '{name}' must use only lowercase letters, digits, and single hyphens, "
                "and must not start or end with a hyphen"
            )
        if name != skill_dir.resolve().name:
            errors.append(f"name '{name}' does not match directory '{skill_dir.resolve().name}'")

    description = data.get("description")
    if not description or not str(description).strip():
        errors.append("description is required")
    elif len(str(description)) > MAX_DESCRIPTION:
        errors.append(f"description has {len(str(description))} characters (max {MAX_DESCRIPTION})")

    metadata = data.get("metadata")
    if metadata is not None:
        if not isinstance(metadata, dict):
            errors.append("metadata must be a map of strings")
        else:
            for key, value in metadata.items():
                if not isinstance(value, str):
                    errors.append(f"metadata value for '{key}' must be a string")
    return errors


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: validate_frontmatter.py SKILL_DIR", file=sys.stderr)
        return 2
    errors = validate(argv[0])
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
