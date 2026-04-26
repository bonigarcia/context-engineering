import unittest

from src.backlog import Idea, score_idea


class IdeaScoreTests(unittest.TestCase):
    def test_score_idea_uses_weighted_formula(self) -> None:
        idea = Idea(title="Inbox triage", impact=4, effort=2, strategic_fit=5)

        self.assertEqual(score_idea(idea), 31)

    def test_score_idea_rejects_out_of_range_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "impact must be between 0 and 5"):
            score_idea(Idea(title="Broken", impact=6, effort=1, strategic_fit=1))


if __name__ == "__main__":
    unittest.main()
