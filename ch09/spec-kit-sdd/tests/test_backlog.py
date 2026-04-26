import unittest

from src.backlog import Idea, score_idea


class IdeaScoreTests(unittest.TestCase):
    def test_score_idea_uses_weighted_formula(self) -> None:
        idea = Idea(title="Roadmap summary", impact=5, effort=1, strategic_fit=4)

        self.assertEqual(score_idea(idea), 35)

    def test_score_idea_rejects_non_integer_components(self) -> None:
        for field_name in ("impact", "effort", "strategic_fit"):
            with self.subTest(field_name=field_name):
                values = {"impact": 4, "effort": 2, "strategic_fit": 3}
                values[field_name] = 2.5

                with self.assertRaisesRegex(ValueError, f"{field_name} must be an integer"):
                    score_idea(Idea(title="Broken", **values))

    def test_score_idea_rejects_negative_effort(self) -> None:
        with self.assertRaisesRegex(ValueError, "effort must be between 0 and 5"):
            score_idea(Idea(title="Broken", impact=4, effort=-1, strategic_fit=3))


if __name__ == "__main__":
    unittest.main()
