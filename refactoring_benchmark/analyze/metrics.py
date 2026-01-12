"""Metric functions for evaluation results."""

from pathlib import Path
from typing import Callable

from refactoring_benchmark.evaluation.models import EvaluationResult
from refactoring_benchmark.utils.models import ReducedInstanceRow
from refactoring_benchmark.coverage.precision import calculate_precision_eval_result, InstanceAgentPrecision

# Type alias for metric functions
# Returns float value in [0, 1] range, or None if metric cannot be computed
MetricFunction = Callable[[EvaluationResult], float | None]

# Hardcoded path for pseudo agents
PSEUDO_AGENTS_DIR = Path("./output_pseudo_agents")


def metric_ifr(result: EvaluationResult) -> float:
    """Total IFR metric (0-1 range)."""
    return result.agent_rule_metrics.ifr


def metric_test_success(result: EvaluationResult) -> float | None:
    """Test success metric (1.0 if valid, 0.0 otherwise, None if no test data)."""
    if result.agent_test_metrics is None:
        return None
    return 1.0 if result.agent_test_metrics.is_valid else 0.0


def _calculate_precision(result: EvaluationResult) -> InstanceAgentPrecision | None:
    """Helper to calculate precision metrics (requires ./output_pseudo_agents/)."""
    if not PSEUDO_AGENTS_DIR.exists():
        raise ValueError(
            f"Precision metrics require pseudo agents but directory {PSEUDO_AGENTS_DIR.absolute()} does not exist.\n"
            f"Hint: Run 'python -m refactoring_benchmark.tools.create_pseudo_agents --agent null --agent golden --output-dir output_pseudo_agents' first."
        )

    return calculate_precision_eval_result(
        result,
    )


def metric_precision_added(result: EvaluationResult) -> float | None:
    """Precision of added lines (requires ./output_pseudo_agents/)."""
    precision_result = _calculate_precision(result)
    return precision_result.metrics.precision_added if precision_result else None


def metric_precision_removed(result: EvaluationResult) -> float | None:
    """Precision of removed lines (requires ./output_pseudo_agents/)."""
    precision_result = _calculate_precision(result)
    return precision_result.metrics.precision_removed if precision_result else None


def metric_precision_overall(result: EvaluationResult) -> float | None:
    """Overall precision (requires ./output_pseudo_agents/)."""
    precision_result = _calculate_precision(result)
    return precision_result.metrics.precision_overall if precision_result else None


# Registry of available metrics
METRICS: dict[str, MetricFunction] = {
    "ifr": metric_ifr,
    "test_success": metric_test_success,
    "precision_added": metric_precision_added,
    "precision_removed": metric_precision_removed,
    "precision_overall": metric_precision_overall,
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
