from importlib import util
from pathlib import Path
import unittest


def load_example_module():
    path = Path(__file__).with_name("structured_output.py")
    spec = util.spec_from_file_location("structured_output", path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StructuredOutputTests(unittest.TestCase):
    def test_prioritizes_billing_requests(self):
        module = load_example_module()

        plan = module._plan_request(
            "Refund needed after being charged twice for my subscription."
        )

        self.assertEqual(plan["priority"], "high")
        self.assertEqual(plan["owner"], "billing")


if __name__ == "__main__":
    unittest.main()
