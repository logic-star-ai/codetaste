"""Metric functions for evaluation results."""

from pathlib import Path
from typing import Callable

from refactoring_benchmark.analyze.diff_stats import parse_diff_file
from refactoring_benchmark.analyze.validation import ValidityStatus, check_test_validity
from refactoring_benchmark.coverage.parse import parse_diff_line_counts_file
from refactoring_benchmark.coverage.precision import (
    InstanceAgentPrecision,
    calculate_precision_eval_result,
)
from refactoring_benchmark.evaluation.models import EvaluationResult

# Type alias for metric functions
# Returns float value in [0, 1] range, or None if metric cannot be computed
MetricFunction = Callable[[EvaluationResult], float | None]


def metric_ifr(result: EvaluationResult) -> float:
    """Total IFR metric (0-1 range)."""
    return result.agent_rule_metrics.ifr


def metric_ifr_added(result: EvaluationResult) -> float:
    """IFR for added lines only (0-1 range)."""
    return result.agent_rule_metrics.positive_ifr


def metric_ifr_removed(result: EvaluationResult) -> float:
    """IFR for removed lines only (0-1 range)."""
    return result.agent_rule_metrics.negative_ifr


def metric_diff_added_lines(result: EvaluationResult) -> int | None:
    diff_path = Path(result.eval_dir.parent) / "prediction.diff"
    try:
        _, lines_added = parse_diff_line_counts_file(diff_path, "base", "predicted")
    except FileNotFoundError:
        return None
    return lines_added


def metric_diff_removed_lines(result: EvaluationResult) -> int | None:
    diff_path = Path(result.eval_dir.parent) / "prediction.diff"
    try:
        lines_removed, _ = parse_diff_line_counts_file(diff_path, "base", "predicted")
    except FileNotFoundError:
        return None
    return lines_removed


def metric_diff_delta_lines(result: EvaluationResult) -> int | None:
    try:
        diff_stat = parse_diff_file(Path(result.eval_dir.parent) / "prediction.diff")
    except FileNotFoundError:
        return None
    return diff_stat.added_lines - diff_stat.removed_lines


def metric_diff_size(result: EvaluationResult) -> int | None:
    """Total diff size (added + removed lines), with precision-style exclusions."""
    diff_path = Path(result.eval_dir.parent) / "prediction.diff"
    try:
        lines_removed, lines_added = parse_diff_line_counts_file(diff_path, "base", "predicted")
    except FileNotFoundError:
        return None
    return lines_added + lines_removed


def metric_test_success(result: EvaluationResult) -> float | None:
    """Test success metric (1.0 if valid, 0.0 otherwise, None if we cannot determine validity)."""
    if check_test_validity(result) == ValidityStatus.VALID:
        return 1.0
    elif check_test_validity(result) in {ValidityStatus.NO_EXEC_ENV, ValidityStatus.NO_BASELINE}:
        return None
    else:
        return 0.0


def metric_strict_ifr_x_test_success(result: EvaluationResult) -> float | None:
    """Strict IFR x Test Success metric (1.0 only if both IFR and test success are perfect)."""
    is_test_success = metric_test_success(result)
    if is_test_success is None:
        return None
    if metric_ifr(result) == 1.0 and is_test_success == 1.0:
        return 1.0
    else:
        return 0.0


def metric_ifr_x_test_success(result: EvaluationResult) -> float | None:
    """Combined IFR x Test Success metric."""
    test_success = metric_test_success(result)
    if test_success is None:
        return None
    return metric_ifr(result) * test_success


def metric_ifr_added_x_test_success(result: EvaluationResult) -> float | None:
    """Combined IFR Added x Test Success metric."""
    test_success = metric_test_success(result)
    if test_success is None:
        return None
    return metric_ifr_added(result) * test_success


def metric_ifr_removed_x_test_success(result: EvaluationResult) -> float | None:
    """Combined IFR Removed x Test Success metric."""
    test_success = metric_test_success(result)
    if test_success is None:
        return None
    return metric_ifr_removed(result) * test_success


def metric_f1_score(result: EvaluationResult) -> float | None:
    """Harmonic mean of precision and instruction following (recall)."""
    p = metric_precision_overall(result)
    r = metric_ifr(result)
    passed = metric_test_success(result)
    if passed is None:
        return None
    if not passed:
        return 0.0
    if p is not None and r is not None:
        if (p + r) == 0:
            return 0.0
        return 2 * (p * r) / (p + r)
    return None


def _calculate_precision(result: EvaluationResult) -> InstanceAgentPrecision | None:
    """Helper to calculate precision metrics (requires pseudo-agent outputs)."""
    return calculate_precision_eval_result(result)


def metric_precision_added(result: EvaluationResult) -> float | None:
    """Precision of added lines (requires pseudo-agent outputs)."""
    precision_result = _calculate_precision(result)
    return precision_result.metrics.precision_added if precision_result else None


def metric_precision_removed(result: EvaluationResult) -> float | None:
    """Precision of removed lines (requires pseudo-agent outputs)."""
    precision_result = _calculate_precision(result)
    return precision_result.metrics.precision_removed if precision_result else None


def metric_precision_overall(result: EvaluationResult) -> float | None:
    """Overall precision (requires pseudo-agent outputs)."""
    precision_result = _calculate_precision(result)
    return precision_result.metrics.precision_overall if precision_result else None


def metric_cost(result: EvaluationResult) -> float | None:
    """Cost in USD (None if not available)."""
    if result.inference_metadata is None:
        return None
    return result.inference_metadata.cost_usd


# Registry of available metrics
METRICS: dict[str, MetricFunction] = {
    "f1": metric_f1_score,
    "ifr": metric_ifr,
    "ifr_x_test_success": metric_ifr_x_test_success,
    "ifr_added_x_test_success": metric_ifr_added_x_test_success,
    "ifr_removed_x_test_success": metric_ifr_removed_x_test_success,
    "strict_ifr_x_test_success": metric_strict_ifr_x_test_success,
    "f1_score": metric_f1_score,
    "ifr_added": metric_ifr_added,
    "ifr_removed": metric_ifr_removed,
    "diff_added_lines": metric_diff_added_lines,
    "diff_removed_lines": metric_diff_removed_lines,
    "diff_delta_lines": metric_diff_delta_lines,
    "diff_size": metric_diff_size,
    "test_success": metric_test_success,
    "precision_added": metric_precision_added,
    "precision_removed": metric_precision_removed,
    "precision_overall": metric_precision_overall,
    "cost": metric_cost,
}

# All available metrics
ALL_METRICS: list[str] = list(METRICS.keys())


def get_metric_function(metric_name: str) -> MetricFunction:
    """Get metric function by name.

    Args:
        metric_name: Name of the metric (e.g., "ifr", "test_success", "precision_overall")

    Returns:
        Metric function

    Raises:
        ValueError: If metric name is not recognized
    """
    if metric_name not in METRICS:
        available = ", ".join(ALL_METRICS)
        raise ValueError(f"Unknown metric '{metric_name}'. Available metrics: {available}")
    return METRICS[metric_name]
