import unittest

from src.backlog import Idea, score_idea


class IdeaScoreTests(unittest.TestCase):
    def test_score_idea_uses_weighted_formula(self) -> None:
        idea = Idea(title="Release notes", impact=3, effort=1, strategic_fit=4)

        self.assertEqual(score_idea(idea), 25)

    def test_score_idea_rejects_out_of_range_values(self) -> None:
        idea = Idea(title="Release notes", impact=6, effort=1, strategic_fit=4)

        with self.assertRaisesRegex(ValueError, "impact must be between 0 and 5"):
            score_idea(idea)


if __name__ == "__main__":
    unittest.main()
