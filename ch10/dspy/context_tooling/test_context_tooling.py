from importlib import util
from pathlib import Path
import unittest


def load_example_module():
    path = Path(__file__).with_name("context_tooling.py")
    spec = util.spec_from_file_location("context_tooling", path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ContextToolingTests(unittest.TestCase):
    def test_retrieves_matching_local_context(self):
        module = load_example_module()

        context = module._lookup_context(
            "How do I reset my password?",
            module.KNOWLEDGE_BASE,
        )

        self.assertIn("Reset password", context)
        self.assertIn("self-service", context)


if __name__ == "__main__":
    unittest.main()
