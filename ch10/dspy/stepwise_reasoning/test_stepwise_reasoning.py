from importlib import util
from pathlib import Path
import unittest


def load_example_module():
    path = Path(__file__).with_name("stepwise_reasoning.py")
    spec = util.spec_from_file_location("stepwise_reasoning", path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StepwiseReasoningTests(unittest.TestCase):
    def test_produces_reasoning_and_answer_helpers(self):
        module = load_example_module()

        response = module._reason_about(
            "How should we handle the product launch this week?"
        )

        self.assertIn("launch request", response["reasoning"])
        self.assertIn("release steps", response["answer"])


if __name__ == "__main__":
    unittest.main()
