from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def load_example_module():
    path = ROOT / "ch10" / "deepagents" / "deep_agent_example.py"
    spec = spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_readme_lists_all_examples():
    readme = (ROOT / "ch10" / "deepagents" / "README.md").read_text(encoding="utf-8")

    example_lines = [line.strip() for line in readme.splitlines() if line.strip().startswith("- `")]
    assert [line.split("`")[1] for line in example_lines] == [
        "deep_agent_example",
        "filesystem_context",
        "subagent_delegation",
        "human_approval",
    ]


def test_anchor_example_uses_chapter_7_call_shape(monkeypatch):
    module = load_example_module()
    captured = {}

    class DummyAgent:
        def invoke(self, *_args, **_kwargs):
            return None

    def fake_create_deep_agent(**kwargs):
        captured.update(kwargs)
        return DummyAgent()

    monkeypatch.setattr(module, "create_deep_agent", fake_create_deep_agent)
    monkeypatch.setattr(module.os.path, "exists", lambda *_args, **_kwargs: False)

    module.main()

    assert captured == {
        "model": "openai:gpt-4o",
        "tools": [],
        "system_prompt": "You are a senior analyst capable of complex research and planning.",
    }
