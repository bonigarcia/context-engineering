import builtins
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import count_tokens as ct

REAL_IMPORT = builtins.__import__


def no_tiktoken(name, *args, **kwargs):
    if name == "tiktoken":
        raise ImportError
    return REAL_IMPORT(name, *args, **kwargs)


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with mock.patch("builtins.__import__", side_effect=no_tiktoken), redirect_stdout(out), redirect_stderr(err):
        try:
            code = ct.main(argv)
        except SystemExit as exit_:
            code = exit_.code
    return code, out.getvalue(), err.getvalue()


class CountTokensTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        return path

    def test_estimate_mode_rounds_up(self):
        path = self.write("ten.txt", "0123456789")
        code, out, _ = run([f"instructions={path}"])
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(data["method"], "estimate:chars/4")
        self.assertEqual(data["sources"], [{"source": "instructions", "files": 1, "tokens": 3}])
        self.assertEqual(data["total"], 3)

    def test_directory_source_sums_files(self):
        self.write("kb/a.md", "a" * 8)
        self.write("kb/sub/b.md", "b" * 4)
        code, out, _ = run([f"knowledge={self.root / 'kb'}"])
        self.assertEqual(json.loads(out)["sources"][0], {"source": "knowledge", "files": 2, "tokens": 3})

    def test_over_budget(self):
        path = self.write("big.txt", "x" * 40)
        _, out, _ = run(["--budget", "5", f"memory={path}"])
        data = json.loads(out)
        self.assertEqual(data["budget"], 5)
        self.assertTrue(data["over_budget"])

    def test_no_budget_gives_null(self):
        path = self.write("small.txt", "x")
        _, out, _ = run([f"memory={path}"])
        data = json.loads(out)
        self.assertIsNone(data["budget"])
        self.assertIsNone(data["over_budget"])

    def test_crlf_and_non_ascii(self):
        path = self.write("w.txt", "café\r\nnaïve\r\n")
        code, out, _ = run([f"instructions={path}"])
        self.assertEqual(code, 0)
        self.assertGreater(json.loads(out)["total"], 0)

    def test_malformed_argument_exits_2(self):
        code, _, err = run(["no-equals-sign"])
        self.assertEqual(code, 2)
        self.assertIn("SOURCE=PATH", err)

    def test_missing_path_exits_2(self):
        code, _, err = run([f"tools={self.root / 'missing.json'}"])
        self.assertEqual(code, 2)
        self.assertIn("not found", err)


if __name__ == "__main__":
    unittest.main()
