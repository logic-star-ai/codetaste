import json
from pathlib import Path
from types import SimpleNamespace

from refactoring_benchmark.analyze.metrics import metric_cost
from refactoring_benchmark.inference.models import InferenceMetadata


def _make_result(run_dir: Path, inference_cost: float | None):
    metadata = None if inference_cost is None else InferenceMetadata(cost_usd=inference_cost, finish_reason="success")
    return SimpleNamespace(
        inference_metadata=metadata,
        eval_dir=run_dir / "evaluation",
    )


def test_metric_cost_returns_none_when_inference_metadata_missing(tmp_path: Path):
    run_dir = tmp_path / "run"
    (run_dir / "evaluation").mkdir(parents=True)
    (run_dir / "plan_metadata.json").write_text(
        json.dumps({"cost_usd": 2.0, "finish_reason": "success"}),
        encoding="utf-8",
    )

    result = _make_result(run_dir, inference_cost=None)
    assert metric_cost(result) is None


def test_metric_cost_includes_plan_metadata_cost(tmp_path: Path):
    run_dir = tmp_path / "run"
    (run_dir / "evaluation").mkdir(parents=True)
    (run_dir / "plan_metadata.json").write_text(
        json.dumps({"cost_usd": 0.75, "finish_reason": "success"}),
        encoding="utf-8",
    )

    result = _make_result(run_dir, inference_cost=1.25)
    assert metric_cost(result) == 2.0


def test_metric_cost_includes_multiplan_generation_and_judge_cost(tmp_path: Path):
    run_dir = tmp_path / "run"
    (run_dir / "evaluation").mkdir(parents=True)
    (run_dir / "multiplan_generation_metadata.json").write_text(
        json.dumps({"cost_usd": 0.9, "finish_reason": "success"}),
        encoding="utf-8",
    )
    (run_dir / "multiplan_metadata.json").write_text(
        json.dumps(
            {
                "start_time": "2025-01-01T00:00:00Z",
                "finish_reason": "success",
                "judge_cost_usd": 0.4,
            }
        ),
        encoding="utf-8",
    )

    result = _make_result(run_dir, inference_cost=1.7)
    assert metric_cost(result) == 3.0

