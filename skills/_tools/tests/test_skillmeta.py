import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skillmeta import FrontmatterError, load_skills, parse_frontmatter  # noqa: E402

SAMPLE = """---
name: tool-reviewer
description: Reviews tool definitions.
license: Apache-2.0
metadata:
  chapter: "4"
  chapter-title: 'Tools in AI agents'
---

# Body
"""


def write_skill(root, dirname, chapter=None):
    skill_dir = root / dirname
    skill_dir.mkdir(parents=True)
    meta = f'metadata:\n  chapter: "{chapter}"\n' if chapter else ""
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {dirname}\ndescription: d\n{meta}---\nbody\n", encoding="utf-8"
    )


class ParseFrontmatterTest(unittest.TestCase):
    def test_parses_flat_and_metadata(self):
        data, body = parse_frontmatter(SAMPLE)
        self.assertEqual(data["name"], "tool-reviewer")
        self.assertEqual(data["license"], "Apache-2.0")
        self.assertEqual(data["metadata"], {"chapter": "4", "chapter-title": "Tools in AI agents"})
        self.assertEqual(body.strip(), "# Body")

    def test_quoted_values(self):
        data, _ = parse_frontmatter('---\nname: "a"\ndescription: \'Use it: always\'\n---\n')
        self.assertEqual(data["name"], "a")
        self.assertEqual(data["description"], "Use it: always")

    def test_crlf_input(self):
        self.assertEqual(parse_frontmatter(SAMPLE.replace("\n", "\r\n")), parse_frontmatter(SAMPLE))

    def test_missing_fence_raises(self):
        with self.assertRaises(FrontmatterError):
            parse_frontmatter("name: x\n")

    def test_list_value_raises(self):
        with self.assertRaises(FrontmatterError):
            parse_frontmatter("---\nname: x\nallowed-tools:\n  - Bash\n---\n")


class LoadSkillsTest(unittest.TestCase):
    def test_load_skills_sorted_and_skips_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root, "zeta", "4")
            write_skill(root, "alpha", "2")
            write_skill(root, "_tools")
            write_skill(root, "evals")
            skills = load_skills(root)
        self.assertEqual([s["name"] for s in skills], ["alpha", "zeta"])
        self.assertEqual(skills[0]["path"], "skills/alpha")


if __name__ == "__main__":
    unittest.main()
