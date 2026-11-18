import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import prompt  # noqa: E402


def make_tree(root):
    skill = root / "demo-skill"
    (skill / "references").mkdir(parents=True)
    (skill / "examples" / "bundle").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        '---\nname: demo-skill\ndescription: Use for demos.\nmetadata:\n  chapter: "2"\n---\nDo the demo.\n',
        encoding="utf-8",
    )
    (skill / "references" / "checklist.md").write_text("Rule one.\n", encoding="utf-8")
    (skill / "examples" / "input.md").write_bytes("café\r\nline two\r\n".encode("utf-8"))
    (skill / "examples" / "bundle" / "b.txt").write_text("B\n", encoding="utf-8")
    (skill / "examples" / "bundle" / "a.txt").write_text("A\n", encoding="utf-8")
    other = root / "other-skill"
    other.mkdir()
    (other / "SKILL.md").write_text("---\nname: other-skill\ndescription: Use for others.\n---\nx\n", encoding="utf-8")


class PromptTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        make_tree(self.root)
        self.old_root = prompt.SKILLS_ROOT
        prompt.SKILLS_ROOT = self.root

    def tearDown(self):
        prompt.SKILLS_ROOT = self.old_root
        self.tmp.cleanup()

    def context(self, artifacts, request="Review it."):
        return {"vars": {"skill": "demo-skill", "artifacts": artifacts, "request": request}}

    def test_build_prompt_includes_skill_and_references(self):
        system, user = prompt.build_prompt(self.context(["input.md"]))
        self.assertEqual(system["role"], "system")
        self.assertIn("Do the demo.", system["content"])
        self.assertIn("Rule one.", system["content"])
        self.assertNotIn("description: Use for demos.", system["content"])
        self.assertEqual(user["role"], "user")
        self.assertTrue(user["content"].startswith("Review it."))
        self.assertIn("=== FILE: input.md ===", user["content"])

    def test_build_prompt_reads_crlf_utf8(self):
        _, user = prompt.build_prompt(self.context(["input.md"]))
        self.assertIn("café\nline two\n", user["content"])
        self.assertNotIn("\r", user["content"])

    def test_build_prompt_expands_directory(self):
        _, user = prompt.build_prompt(self.context(["bundle"]))
        content = user["content"]
        self.assertLess(content.index("=== FILE: bundle/a.txt ==="), content.index("=== FILE: bundle/b.txt ==="))

    def test_build_prompt_accepts_comma_separated_artifacts(self):
        _, user = prompt.build_prompt(self.context("input.md, bundle"))
        self.assertIn("=== FILE: input.md ===", user["content"])
        self.assertIn("=== FILE: bundle/a.txt ===", user["content"])

    def test_build_prompt_missing_artifact_raises(self):
        with self.assertRaises(FileNotFoundError):
            prompt.build_prompt(self.context(["nope.md"]))

    def test_activation_prompt_lists_all_skills(self):
        system, user = prompt.build_activation_prompt({"vars": {"request": "Do a demo"}})
        self.assertIn("- demo-skill: Use for demos.", system["content"])
        self.assertIn("- other-skill: Use for others.", system["content"])
        self.assertIn("none", system["content"])
        self.assertEqual(user["content"], "Do a demo")


if __name__ == "__main__":
    unittest.main()
