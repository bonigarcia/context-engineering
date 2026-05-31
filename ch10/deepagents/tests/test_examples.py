from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_example_module(rel_path: str):
    root = Path(__file__).resolve().parents[3]
    path = root / rel_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_research_harness_builder_uses_deepagents(monkeypatch):
    seen = {}

    def fake_create_deep_agent(**kwargs):
        seen.update(kwargs)
        return object()

    research_harness = load_example_module("ch10/deepagents/research_harness/research_harness.py")
    monkeypatch.setattr(research_harness, "create_deep_agent", fake_create_deep_agent)

    agent = research_harness.build_agent(Path("C:/repo"))

    assert agent is not None
    assert seen["model"] == "openai:gpt-5.4"
    assert seen["system_prompt"].startswith("You are a concise research assistant")
    assert {tool.name for tool in seen["tools"]} == {
        "list_markdown_files",
        "read_markdown_file",
        "summarize_bounded_notes",
    }
    assert all(callable(tool) for tool in seen["tools"])


def test_filesystem_context_sets_memory_and_backend(monkeypatch):
    seen = {}

    def fake_create_deep_agent(**kwargs):
        seen.update(kwargs)
        return object()

    filesystem_context = load_example_module("ch10/deepagents/filesystem_context/filesystem_context.py")
    monkeypatch.setattr(filesystem_context, "create_deep_agent", fake_create_deep_agent)
    monkeypatch.setattr(filesystem_context, "build_store", lambda: object())
    monkeypatch.setattr(filesystem_context, "build_backend", lambda: object())

    agent = filesystem_context.build_agent()

    assert agent is not None
    assert seen["model"] == "openai:gpt-5.4"
    assert seen["memory"] == ["/memories/AGENTS.md"]
    assert seen["store"] is not None
    assert seen["backend"] is not None


def test_filesystem_context_fails_cleanly_without_deps(monkeypatch):
    filesystem_context = load_example_module("ch10/deepagents/filesystem_context/filesystem_context.py")
    monkeypatch.setattr(filesystem_context, "create_deep_agent", None)

    try:
        filesystem_context.build_agent()
    except RuntimeError as exc:
        assert "filesystem_context requires deepagents" in str(exc)
    else:
        raise AssertionError("Expected build_agent() to fail without DeepAgents")
