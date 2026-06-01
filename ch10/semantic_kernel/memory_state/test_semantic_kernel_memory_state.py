from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from semantic_kernel_memory_state import answer_favorite_topic, remember_favorite_topic


def test_remember_and_recall_favorite_topic():
    state = {}

    remember_favorite_topic(state, "semantic kernels")

    assert answer_favorite_topic(state) == "semantic kernels"
