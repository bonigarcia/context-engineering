import unittest
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN = {
    chr(0x2013): "en dash",
    chr(0x2014): "em dash",
    chr(0x2018): "curly quote",
    chr(0x2019): "curly apostrophe",
    chr(0x201C): "curly quote",
    chr(0x201D): "curly quote",
}
PATTERNS = ("*.md", "*.yaml", "*.py", "*.json", "*.txt")


class StyleTest(unittest.TestCase):
    def test_no_forbidden_characters(self):
        problems = []
        for pattern in PATTERNS:
            for path in SKILLS_ROOT.rglob(pattern):
                if path.parent.name == "evals" and path.name.startswith("results"):
                    continue
                text = path.read_text(encoding="utf-8")
                for number, line in enumerate(text.splitlines(), start=1):
                    for char, label in FORBIDDEN.items():
                        if char in line:
                            problems.append(f"{path.relative_to(SKILLS_ROOT)}:{number}: {label}")
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
