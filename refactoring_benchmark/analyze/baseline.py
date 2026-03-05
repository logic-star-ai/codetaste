"""Baseline test results utilities."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata
from refactoring_benchmark.evaluation.models import TestMetrics
from refactoring_benchmark.utils.paths import BASELINE_RESULTS_DIR

BASELINE_AGENT_IDS = ("golden_agent", "null_agent")


@dataclass(frozen=True)
class BaselineBounds:
    """Min/Max bounds derived from baseline test runs."""

    min_passed: int
    max_failed: int


def baseline_instance_dir(instance: ExecutionInstanceMetadata, base_dir: Path = BASELINE_RESULTS_DIR) -> Path:
    """Return baseline results directory for an instance."""
    short_hash = instance.base_hash[:8]
    return base_dir / instance.owner / instance.repo / short_hash


def _baseline_files(instance: ExecutionInstanceMetadata, base_dir: Path = BASELINE_RESULTS_DIR) -> list[Path]:
    instance_dir = baseline_instance_dir(instance, base_dir=base_dir)
    return [instance_dir / f"{agent_id}.jsonl" for agent_id in BASELINE_AGENT_IDS]


def load_baseline_metrics(
    instance: ExecutionInstanceMetadata, base_dir: Path = BASELINE_RESULTS_DIR
) -> list[TestMetrics]:
    """Load baseline test metrics for an instance from jsonl files."""
    metrics: list[TestMetrics] = []
    for path in _baseline_files(instance, base_dir=base_dir):
        if not path.exists():
            continue
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if data is None:
                            continue
                        metrics.append(TestMetrics(**data))
                    except Exception:
                        continue
        except Exception:
            continue
    return metrics


def compute_baseline_bounds(metrics: Iterable[TestMetrics]) -> BaselineBounds | None:
    """Compute baseline min/max bounds from a collection of test metrics."""
    metrics_list = list(metrics)
    if not metrics_list:
        return None
    min_passed = min(metric.passed for metric in metrics_list)
    max_failed = max(metric.failed for metric in metrics_list)
    return BaselineBounds(min_passed=min_passed, max_failed=max_failed)


def load_baseline_bounds(
    instance: ExecutionInstanceMetadata, base_dir: Path = BASELINE_RESULTS_DIR
) -> BaselineBounds | None:
    """Load baseline metrics for an instance and compute bounds."""
    metrics = load_baseline_metrics(instance, base_dir=base_dir)
    return compute_baseline_bounds(metrics)
