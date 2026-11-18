import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import assertions  # noqa: E402


def report(findings, **extra):
    body = {"skill": "demo", "summary": "s", "findings": findings, **extra}
    return "## Summary\ns\n\n```json\n" + json.dumps(body) + "\n```\n"


FINDING = {
    "severity": "high",
    "location": "tools.json, find_orders",
    "problem": "Overlaps with search_orders.",
    "fix": "Merge the two tools.",
    "book_section": "Chapter 4, Tool definitions as contracts",
}


def ctx(**vars_):
    return {"vars": vars_}


class CheckReportTest(unittest.TestCase):
    def test_check_report_pass(self):
        result = assertions.check_report(
            report([FINDING]), ctx(required=[{"keywords": ["search_orders", "find_orders"]}])
        )
        self.assertTrue(result["pass"], result["reason"])
        self.assertEqual(result["score"], 1.0)

    def test_check_report_no_json(self):
        result = assertions.check_report("## Summary\nNo JSON here.", ctx())
        self.assertFalse(result["pass"])
        self.assertIn("no JSON block", result["reason"])

    def test_check_report_uses_last_block(self):
        first = report([])
        last = report([FINDING])
        result = assertions.check_report(first + last, ctx(required=[{"keywords": ["merge"]}]))
        self.assertTrue(result["pass"], result["reason"])

    def test_check_report_bad_severity(self):
        bad = dict(FINDING, severity="critical")
        result = assertions.check_report(report([bad]), ctx())
        self.assertFalse(result["pass"])
        self.assertIn("severity", result["reason"])

    def test_check_report_missing_required(self):
        result = assertions.check_report(report([FINDING]), ctx(required=[{"keywords": ["get_data"]}]))
        self.assertFalse(result["pass"])
        self.assertEqual(result["score"], 0.0)
        self.assertIn("get_data", result["reason"])

    def test_check_report_forbidden_match(self):
        result = assertions.check_report(
            report([FINDING]), ctx(forbidden=[{"keywords": [""], "location": "find_orders"}])
        )
        self.assertFalse(result["pass"])
        self.assertIn("forbidden", result["reason"])

    def test_check_report_location_filter(self):
        result = assertions.check_report(
            report([FINDING]), ctx(required=[{"keywords": ["overlap"], "location": "get_customer"}])
        )
        self.assertFalse(result["pass"])

    def test_check_report_alternative_keywords(self):
        result = assertions.check_report(report([FINDING]), ctx(required=[{"keywords": ["duplicate|overlap"]}]))
        self.assertTrue(result["pass"], result["reason"])

    def test_check_report_extra_mismatch(self):
        result = assertions.check_report(report([FINDING], recommendation="cag"), ctx(extra={"recommendation": "rag"}))
        self.assertFalse(result["pass"])
        self.assertIn("recommendation", result["reason"])

    def test_check_report_extra_accepts_list_of_allowed_values(self):
        result = assertions.check_report(
            report([FINDING], recommendation="cag"), ctx(extra={"recommendation": ["cag", "context-stuffing"]})
        )
        self.assertTrue(result["pass"], result["reason"])

    def test_check_report_non_dict_finding_fails_cleanly(self):
        result = assertions.check_report('```json\n{"findings": ["x"]}\n```', ctx())
        self.assertFalse(result["pass"])
        self.assertIn("finding 0", result["reason"])

    def test_check_report_findings_missing(self):
        text = '```json\n{"summary": "s"}\n```'
        result = assertions.check_report(text, ctx())
        self.assertFalse(result["pass"])
        self.assertIn("findings", result["reason"])


class CheckCasesTest(unittest.TestCase):
    def cases(self, categories):
        return [{"description": "d", "category": c, "vars": {}, "assert": []} for c in categories]

    def test_check_cases_pass(self):
        text = report([], cases=self.cases(["happy-path", "policy-violation", "adversarial", "edge-case", "happy-path"]))
        result = assertions.check_cases(
            text, ctx(min_cases=5, categories=["happy-path", "policy-violation", "adversarial"])
        )
        self.assertTrue(result["pass"], result["reason"])

    def test_check_cases_too_few(self):
        text = report([], cases=self.cases(["happy-path"]))
        result = assertions.check_cases(text, ctx(min_cases=5, categories=[]))
        self.assertFalse(result["pass"])
        self.assertIn("5", result["reason"])

    def test_check_cases_accepts_comma_separated_categories(self):
        text = report([], cases=self.cases(["happy-path"] * 5))
        result = assertions.check_cases(text, ctx(min_cases=5, categories="happy-path, adversarial"))
        self.assertFalse(result["pass"])
        self.assertIn("adversarial", result["reason"])
        self.assertNotIn("category h", result["reason"])

    def test_check_cases_missing_category(self):
        text = report([], cases=self.cases(["happy-path"] * 5))
        result = assertions.check_cases(text, ctx(min_cases=5, categories=["adversarial"]))
        self.assertFalse(result["pass"])
        self.assertIn("adversarial", result["reason"])


class CheckDesignTest(unittest.TestCase):
    def test_check_design_accepts_strings(self):
        text = report([], design={"long_term_memory": ["seat preference"], "workflow_state": ["booking step"]})
        self.assertTrue(assertions.check_design(text, ctx())["pass"])

    def test_check_design_accepts_objects(self):
        text = report([], design={"long_term_memory": [{"kind": "Seat preference"}], "session_state": [{"kind": "current booking step"}]})
        self.assertTrue(assertions.check_design(text, ctx())["pass"])

    def test_check_design_missing_preference(self):
        text = report([], design={"long_term_memory": ["transcripts"], "workflow_state": ["booking"]})
        result = assertions.check_design(text, ctx())
        self.assertFalse(result["pass"])
        self.assertIn("long_term_memory", result["reason"])

    def test_check_design_absent(self):
        self.assertFalse(assertions.check_design(report([]), ctx())["pass"])


class CheckActivationTest(unittest.TestCase):
    def test_check_activation_normalizes(self):
        self.assertTrue(assertions.check_activation(" `Tool-Reviewer`.\n", ctx(expected="tool-reviewer"))["pass"])

    def test_check_activation_wrong(self):
        self.assertFalse(assertions.check_activation("none", ctx(expected="tool-reviewer"))["pass"])


if __name__ == "__main__":
    unittest.main()
