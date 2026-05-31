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


def test_reranking_builds_pipeline_and_orders_relevant_docs_first():
    module = load_module("reranking/haystack_reranking.py")

    pipeline = module.build_pipeline()

    assert isinstance(pipeline, Pipeline)
    result = module.run_query("Where do I find important notes?")
    assert result.splitlines()[1].startswith("- Important notes")


def test_query_expansion_builds_pipeline_and_combines_variants():
    module = load_module("query_expansion/haystack_query_expansion.py")

    pipeline = module.build_pipeline()

    assert isinstance(pipeline, Pipeline)
    result = module.run_query("sync notes")
    assert "sync" in result.lower()
    assert "backup" in result.lower()


def test_pipeline_composition_builds_pipeline_and_runs_all_stages():
    module = load_module("pipeline_composition/haystack_pipeline_composition.py")

    pipeline = module.build_pipeline()

    assert isinstance(pipeline, Pipeline)
    result = module.run_query("organize notes")
    assert "pipeline" in result.lower()
