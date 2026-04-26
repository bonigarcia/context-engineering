import unittest

from src.backlog import Idea, score_idea


class IdeaScoreTests(unittest.TestCase):
    def test_score_idea_uses_weighted_formula(self) -> None:
        idea = Idea(title="Customer import", impact=5, effort=3, strategic_fit=4)

        self.assertEqual(score_idea(idea), 31)

    def test_score_idea_rejects_non_integer_component(self) -> None:
        idea = Idea(title="Customer import", impact=4.5, effort=3, strategic_fit=4)

        with self.assertRaises(ValueError):
            score_idea(idea)


if __name__ == "__main__":
    unittest.main()
