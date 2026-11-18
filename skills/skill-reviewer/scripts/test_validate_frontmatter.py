import builtins
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import validate_frontmatter as vf


def make_skill(root, dirname, frontmatter, newline="\n"):
    skill_dir = Path(root) / dirname
    skill_dir.mkdir()
    text = "---\n" + frontmatter + "---\n\n# Body\n"
    (skill_dir / "SKILL.md").write_bytes(text.replace("\n", newline).encode("utf-8"))
    return skill_dir


def run(skill_dir):
    out = io.StringIO()
    with redirect_stdout(out):
        code = vf.main([str(skill_dir)])
    return code, out.getvalue()


VALID = "name: good-skill\ndescription: Use when X. Do not use when Y.\n"


class ValidateFrontmatterTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_skill_prints_ok(self):
        code, out = run(make_skill(self.root, "good-skill", VALID))
        self.assertEqual((code, out.strip()), (0, "OK"))

    def test_bad_name_and_directory_mismatch(self):
        code, out = run(make_skill(self.root, "pdf_helper", "name: PDF Helper\ndescription: d\n"))
        self.assertEqual(code, 1)
        self.assertIn("ERROR: name 'PDF Helper' must use only lowercase", out)
        self.assertIn("ERROR: name 'PDF Helper' does not match directory 'pdf_helper'", out)

    def test_empty_description(self):
        code, out = run(make_skill(self.root, "a", "name: a\ndescription:\n"))
        self.assertEqual(code, 1)
        self.assertIn("ERROR: description is required", out)

    def test_description_too_long(self):
        code, out = run(make_skill(self.root, "a", "name: a\ndescription: " + "x" * 1025 + "\n"))
        self.assertEqual(code, 1)
        self.assertIn("ERROR: description has 1025 characters (max 1024)", out)

    def test_list_value_without_yaml_is_unparseable(self):
        skill = make_skill(self.root, "a", "name: a\ndescription: d\nallowed-tools:\n  - Bash\n")
        real_import = builtins.__import__

        def no_yaml(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=no_yaml):
            code, out = run(skill)
        self.assertEqual(code, 1)
        self.assertIn("ERROR: cannot parse frontmatter:", out)

    def test_unquoted_colon_without_yaml_is_unparseable(self):
        skill = make_skill(self.root, "a", "name: a\ndescription: Reviews things. Use when: the user asks.\n")
        real_import = builtins.__import__

        def no_yaml(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=no_yaml):
            code, out = run(skill)
        self.assertEqual(code, 1)
        self.assertIn("quote it", out)

    def test_quoted_colon_without_yaml_is_valid(self):
        skill = make_skill(self.root, "a", 'name: a\ndescription: "Use when: the user asks."\n')
        real_import = builtins.__import__

        def no_yaml(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=no_yaml):
            code, out = run(skill)
        self.assertEqual((code, out.strip()), (0, "OK"))

    def test_crlf_file_is_valid(self):
        code, out = run(make_skill(self.root, "good-skill", VALID, newline="\r\n"))
        self.assertEqual((code, out.strip()), (0, "OK"))

    def test_missing_skill_file(self):
        empty = Path(self.root) / "empty"
        empty.mkdir()
        code, out = run(empty)
        self.assertEqual(code, 1)
        self.assertIn("ERROR: SKILL.md not found", out)


if __name__ == "__main__":
    unittest.main()
