from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def load_example_module(rel_path: str):
    path = ROOT / rel_path
    spec = spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_readme_lists_all_examples():
    readme = (ROOT / "ch10" / "deepagents" / "README.md").read_text(encoding="utf-8")

    parts = readme.split("## Included examples", 1)
    assert len(parts) == 2, "README missing Included examples section"
    section = parts[1].split("\n## ", 1)[0]
    example_lines = [line.strip() for line in section.splitlines() if line.strip().startswith("- ")]

    assert example_lines == [
        "- [deep_agent_example](./deep_agent_example/README.md) - the chapter 7-style orchestration anchor",
        "- [filesystem_context](./filesystem_context/README.md) - filesystem-backed context and memory",
        "- [subagent_delegation](./subagent_delegation/README.md) - delegated work with isolated subagents",
        "- [human_approval](./human_approval/README.md) - interrupt-based approval for sensitive tool calls",
    ]


def test_anchor_example_uses_chapter_7_call_shape(monkeypatch):
    module = load_example_module("ch10/deepagents/deep_agent_example.py")
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


def test_build_agent_wires_filesystem_context_backend_and_memory(monkeypatch):
    module = load_example_module("ch10/deepagents/filesystem_context/filesystem_context.py")

    sentinel_backend = object()
    sentinel_store = object()
    captured = {}

    def fake_create_deep_agent(**kwargs):
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(module, "create_deep_agent", fake_create_deep_agent)
    monkeypatch.setattr(module, "build_backend", lambda: sentinel_backend)
    monkeypatch.setattr(module, "build_store", lambda: sentinel_store)

    agent = module.build_agent()

    assert agent is not None
    assert captured["model"] == "openai:gpt-5.4"
    assert captured["memory"] == ["/memories/AGENTS.md"]
    assert captured["backend"] is sentinel_backend
    assert captured["store"] is sentinel_store
    assert captured["tools"] == []
    assert "filesystem-like paths" in captured["system_prompt"]


def test_build_agent_configures_two_isolated_subagents(monkeypatch):
    module = load_example_module("ch10/deepagents/subagent_delegation/subagent_delegation.py")
    captured = {}

    def fake_create_deep_agent(**kwargs):
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(module, "create_deep_agent", fake_create_deep_agent)

    agent = module.build_agent()

    assert agent is not None
    assert [subagent["name"] for subagent in captured["subagents"]] == [
        "research-agent",
        "writer-agent",
    ]
    assert "delegate" in captured["system_prompt"].lower() or "task tool" in captured["system_prompt"].lower()


def test_human_approval_build_agent_wires_interrupts_and_checkpointer(monkeypatch):
    module = load_example_module("ch10/deepagents/human_approval/human_approval.py")
    captured = {}

    def fake_create_deep_agent(**kwargs):
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(module, "create_deep_agent", fake_create_deep_agent)
    monkeypatch.setattr(module, "MemorySaver", lambda: "memory-saver")

    agent = module.build_agent()

    assert agent is not None
    assert captured["model"] == "google_genai:gemini-3.5-flash"
    assert captured["tools"] == [module.remove_file]
    assert captured["interrupt_on"] == {"remove_file": True}
    assert captured["checkpointer"] == "memory-saver"


def test_human_approval_build_output_reports_status():
    module = load_example_module("ch10/deepagents/human_approval/human_approval.py")

    assert "Awaiting approval" in module.build_output(False)
    assert "Approved." in module.build_output(True)
