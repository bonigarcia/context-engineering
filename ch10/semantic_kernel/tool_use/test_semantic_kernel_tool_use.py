from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from semantic_kernel_tool_use import lookup_example_code


def test_lookup_example_code_returns_fixed_value():
    assert lookup_example_code() == "SK-TOOL-42"
