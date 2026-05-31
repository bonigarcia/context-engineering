from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from fastapi import FastAPI


ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str):
    path = ROOT / relative_path
    spec = spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_session_memory_builds_agent():
    module = load_module("session_memory/session_memory.py")

    agent = module.build_agent(ROOT / "session_memory")

    assert agent.name == "Session Memory"
    assert agent.session_id == "chapter-session-memory"


def test_knowledge_store_builds_filesystem_knowledge():
    module = load_module("knowledge_store/knowledge_store.py")

    knowledge = module.build_knowledge(ROOT / "knowledge_store")

    assert knowledge.base_dir == str(ROOT / "knowledge_store")
    assert knowledge.max_results == 3


def test_agent_os_service_builds_fastapi_app():
    module = load_module("agent_os_service/agent_os_service.py")

    app = module.build_app(ROOT / "agent_os_service")

    assert isinstance(app, FastAPI)


def test_audit_traces_builds_json_db():
    module = load_module("audit_traces/audit_traces.py")

    db = module.build_trace_db(ROOT / "audit_traces")

    assert Path(db.db_path) == ROOT / "audit_traces" / "audit_traces.json"
