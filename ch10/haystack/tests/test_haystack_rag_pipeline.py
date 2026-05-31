from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from haystack import Pipeline


ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str):
    path = ROOT / relative_path
    spec = spec_from_file_location(path.stem, path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_pipeline_returns_haystack_pipeline():
    module = load_module("rag_pipeline/haystack_rag_pipeline.py")

    pipeline = module.build_pipeline()

    assert isinstance(pipeline, Pipeline)


def test_run_query_returns_retrieved_context():
    module = load_module("rag_pipeline/haystack_rag_pipeline.py")

    answer = module.run_query("How do I keep notes organized?")

    assert "notes" in answer.lower()
