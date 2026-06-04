import unittest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from src.backlog import app, Idea, score_idea


class BacklogApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_score_idea_function_uses_weighted_formula(self) -> None:
        idea = Idea(title="Release notes", impact=3, effort=1, strategic_fit=4)
        self.assertEqual(score_idea(idea), 25)

    def test_score_idea_function_rejects_out_of_range_values(self) -> None:
        with self.assertRaises(ValidationError):
            Idea(title="Release notes", impact=6, effort=1, strategic_fit=4)

    def test_post_score_endpoint_success(self) -> None:
        response = self.client.post(
            "/score",
            json={"title": "FastAPI migration", "impact": 4, "effort": 2, "strategic_fit": 5}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "FastAPI migration")
        self.assertEqual(data["impact"], 4)
        self.assertEqual(data["effort"], 2)
        self.assertEqual(data["strategic_fit"], 5)
        # 4 * 5 + 5 * 3 - 2 * 2 = 20 + 15 - 4 = 31
        self.assertEqual(data["score"], 31)

    def test_post_score_endpoint_validation_error(self) -> None:
        # Test out-of-range value (impact=6)
        response = self.client.post(
            "/score",
            json={"title": "Invalid impact", "impact": 6, "effort": 1, "strategic_fit": 1}
        )
        self.assertEqual(response.status_code, 422)

        # Test missing fields
        response = self.client.post(
            "/score",
            json={"title": "Missing fields"}
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
