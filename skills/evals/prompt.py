"""Promptfoo prompt functions for the skills evaluation harness.

build_prompt simulates an agent that has activated one skill: the system
message carries the skill body and its references, and the user message
carries the request plus the artifacts from the skill's examples folder.
"""

import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILLS_ROOT / "_tools"))

from skillmeta import load_skills, parse_frontmatter  # noqa: E402

ACTIVATION_INSTRUCTIONS = (
    "You are the skill router of a coding agent. Below is the list of available skills, "
    "each with its name and description. Read the user request and decide which single skill "
    "the agent should activate. Answer with the skill name only, or with the word none when no "
    "skill fits the request. Do not add any other text."
)


def _read(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def _artifact_files(examples, relative):
    target = examples / relative
    if target.is_dir():
        return sorted(p for p in target.rglob("*") if p.is_file())
    if target.is_file():
        return [target]
    raise FileNotFoundError(f"artifact not found: {target}")


def build_prompt(context):
    variables = context["vars"]
    skill_dir = SKILLS_ROOT / variables["skill"]
    _, body = parse_frontmatter(_read(skill_dir / "SKILL.md"))
    parts = [body.strip()]
    for reference in sorted((skill_dir / "references").glob("*.md")):
        parts.append(f"=== REFERENCE: references/{reference.name} ===\n{_read(reference)}")

    examples = skill_dir / "examples"
    artifacts = variables.get("artifacts") or []
    if isinstance(artifacts, str):
        artifacts = [item.strip() for item in artifacts.split(",") if item.strip()]
    user_parts = [variables["request"].strip()]
    for relative in artifacts:
        for path in _artifact_files(examples, relative):
            user_parts.append(f"=== FILE: {path.relative_to(examples).as_posix()} ===\n{_read(path)}")

    return [
        {"role": "system", "content": "\n\n".join(parts)},
        {"role": "user", "content": "\n\n".join(user_parts)},
    ]


def build_activation_prompt(context):
    lines = [f"- {skill['name']}: {skill['description']}" for skill in load_skills(SKILLS_ROOT)]
    return [
        {"role": "system", "content": ACTIVATION_INSTRUCTIONS + "\n\nAvailable skills:\n" + "\n".join(lines)},
        {"role": "user", "content": context["vars"]["request"]},
    ]
