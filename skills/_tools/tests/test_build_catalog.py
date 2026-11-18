import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_catalog  # noqa: E402


def write_skill(root, name, metadata=None):
    skill = root / name
    skill.mkdir(parents=True)
    meta = ""
    if metadata:
        meta = "metadata:\n" + "".join(f'  {k}: "{v}"\n' for k, v in metadata.items())
    (skill / "SKILL.md").write_text(f'---\nname: {name}\ndescription: "Use for {name}."\n{meta}---\nbody\n', encoding="utf-8")


FULL = {"chapter": "4", "chapter-title": "Tools in AI agents", "input": "Tool schemas", "output": "Findings"}


class BuildCatalogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "skills"
        write_skill(self.root, "tool-reviewer", FULL)
        write_skill(self.root, "skill-reviewer", dict(FULL, chapter="2", **{"chapter-title": "Instructions for AI agents"}))
        (self.root / "_tools").mkdir()
        (self.root / "evals").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_entries_ordered_by_chapter_with_fields(self):
        catalog = build_catalog.build_catalog(self.root)
        self.assertEqual([e["name"] for e in catalog], ["skill-reviewer", "tool-reviewer"])
        self.assertEqual(
            catalog[1],
            {
                "name": "tool-reviewer",
                "description": "Use for tool-reviewer.",
                "chapter": "4",
                "chapterTitle": "Tools in AI agents",
                "input": "Tool schemas",
                "output": "Findings",
                "path": "skills/tool-reviewer",
            },
        )

    def test_skill_without_metadata_is_listed_with_warning(self):
        write_skill(self.root, "bare-skill")
        err = io.StringIO()
        with redirect_stderr(err):
            catalog = build_catalog.build_catalog(self.root)
        bare = next(e for e in catalog if e["name"] == "bare-skill")
        self.assertEqual((bare["chapter"], bare["chapterTitle"], bare["input"], bare["output"]), ("", "", "", ""))
        self.assertIn("warning: bare-skill", err.getvalue())

    def test_write_catalog_uses_crlf_and_trailing_newline(self):
        out = Path(self.tmp.name) / "skills.json"
        count = build_catalog.write_catalog(self.root, out)
        raw = out.read_bytes()
        self.assertEqual(count, 2)
        self.assertTrue(raw.endswith(b"\r\n"))
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
        self.assertEqual(len(json.loads(raw.decode("utf-8"))), 2)


if __name__ == "__main__":
    unittest.main()
