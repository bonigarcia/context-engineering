"""Runnable local-memory example for the Semantic Kernel chapter."""

from __future__ import annotations

import json
from pathlib import Path


STATE_FILE = Path(__file__).with_name("memory_state.json")
DEFAULT_TOPIC = "semantic kernels"


def load_state(path: Path = STATE_FILE) -> dict[str, str]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict[str, str], path: Path = STATE_FILE) -> None:
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def remember_favorite_topic(state: dict[str, str], topic: str) -> dict[str, str]:
    state["favorite_topic"] = topic
    return state


def answer_favorite_topic(state: dict[str, str]) -> str:
    return state["favorite_topic"]


def main() -> None:
    state = load_state()

    if state.get("favorite_topic") != DEFAULT_TOPIC:
        remember_favorite_topic(state, DEFAULT_TOPIC)
        save_state(state)

    print("Remember that my favorite topic is semantic kernels.")
    print("What is my favorite topic?")
    print(answer_favorite_topic(state))


if __name__ == "__main__":
    main()
