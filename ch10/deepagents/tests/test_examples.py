from __future__ import annotations

from importlib import util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_example_module():
    path = ROOT / "filesystem_context" / "filesystem_context.py"
    spec = util.spec_from_file_location("filesystem_context", path)
    assert spec and spec.loader
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_agent_wires_filesystem_context_backend_and_memory(monkeypatch):
    module = load_example_module()

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
