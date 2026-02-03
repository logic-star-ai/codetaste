"""Calculate line-level precision metrics for refactoring changes."""

import json
import os
from pathlib import Path
from typing import Optional
from functools import lru_cache

from refactoring_benchmark.coverage.models import (
    SARIFOpengrep,
    PrecisionMetrics,
    PrecisionMetricsResult,
    InstanceAgentPrecision,
)
from refactoring_benchmark.coverage.parse import parse_diff, parse_sarif
from refactoring_benchmark.evaluation.models import EvaluationResult
from refactoring_benchmark.utils.models import ReducedInstanceRow
from joblib import Memory

cachedir = './.cache_dir'
memory = Memory(cachedir, verbose=1)


def _load_precision_data(
    sarif_negative_path: Path,
    sarif_positive_path: Path,
    diff_path: Path,
) -> PrecisionMetrics:
    """Load and parse SARIF and diff files to create PrecisionMetrics.

    Args:
        sarif_negative_path: Path to negative SARIF file
        sarif_positive_path: Path to positive SARIF file
        diff_path: Path to diff file

    Returns:
        PrecisionMetrics object with parsed data
    """
    # Load SARIF files
    with open(sarif_negative_path) as f:
        sarif_neg = SARIFOpengrep.model_validate(json.load(f))

    with open(sarif_positive_path) as f:
        sarif_pos = SARIFOpengrep.model_validate(json.load(f))

    # Parse SARIF to extract lines (commit values are placeholders)
    lines_matched_by_removal_rules = parse_sarif(sarif_neg, "base")
    lines_matched_by_addition_rules = parse_sarif(sarif_pos, "predicted")

    # Load and parse diff
    diff_content = diff_path.read_text(errors='replace')
    lines_removed, lines_added = parse_diff(diff_content, "base", "predicted")

    # Create PrecisionMetrics object for computation
    return PrecisionMetrics(
        lines_added=lines_added,
        lines_removed=lines_removed,
        lines_matched_by_addition_rules=lines_matched_by_addition_rules,
        lines_matched_by_removal_rules=lines_matched_by_removal_rules,
    )


@lru_cache(maxsize=1024)
def calculate_precision(
    sarif_negative_path: Path,
    sarif_positive_path: Path,
    diff_path: Path,
) -> PrecisionMetricsResult:
    # Convert to string paths for efficient cache key
    paths_str = (str(sarif_negative_path), str(sarif_positive_path), str(diff_path))
    paths = [sarif_negative_path, sarif_positive_path, diff_path]
    mtimes = tuple(os.path.getmtime(p) for p in paths)
    return _cached_calculate_precision(paths_str, mtimes)

@memory.cache
def _cached_calculate_precision(
    paths_str: tuple[str, str, str],
    mtimes: tuple,
) -> PrecisionMetricsResult:
    """
    Calculate line-level precision metrics for refactoring changes.

    Args:
        paths_str: Tuple of (sarif_negative, sarif_positive, diff) path strings
        mtimes: Modification times for cache invalidation

    Returns:
        PrecisionMetricsResult with computed precision scores (optimized for caching)
    """
    # Reconstruct Path objects from string paths
    sarif_negative_path = Path(paths_str[0])
    sarif_positive_path = Path(paths_str[1])
    diff_path = Path(paths_str[2])

    # Load and parse data
    metrics = _load_precision_data(sarif_negative_path, sarif_positive_path, diff_path)

    # Convert to result cachable format
    return PrecisionMetricsResult(
        precision_added=metrics.precision_added,
        precision_removed=metrics.precision_removed,
        precision_overall=metrics.precision_overall,
        lines_added_count=len(metrics.lines_added),
        lines_removed_count=len(metrics.lines_removed),
        relevant_added_count=len(metrics.relevant_added_lines),
        relevant_removed_count=len(metrics.relevant_removed_lines),
    )


def calculate_precision_eval_result(
    result: EvaluationResult,
    null_agent_dir: Path = Path("output_pseudo_agents"),
) -> Optional[InstanceAgentPrecision]:
    """
    Calculate precision metrics for a single instance-agent pair.

    Uses baseline negative SARIF from null_agent (shared across all agents)
    and agent-specific positive SARIF.

    Args:
        result: EvaluationResult object
        null_agent_dir: Directory containing pseudo agents

    Returns:
        InstanceAgentPrecision object with results, or None if files don't exist or calculation fails
    """
    # Check if eval_dir is set
    if result.eval_dir is None:
        return None

    # Construct paths
    instance = ReducedInstanceRow(
        owner=result.instance_metadata.owner,
        repo=result.instance_metadata.repo,
        golden_commit_hash=result.instance_metadata.golden_hash,
        commit_hash=result.instance_metadata.base_hash,
    )
    pseudo_agent_instance_dir = null_agent_dir / instance.owner / instance.repo / instance.short_hash

    # Use null_agent for baseline negative SARIF (bad patterns in base code)
    instance_null_agent_dir = pseudo_agent_instance_dir / "null_agent"
    sarif_negative_path = instance_null_agent_dir / "evaluation" / "rules_negative.sarif"

    # Use agent-specific positive SARIF (good patterns in agent's solution)
    sarif_positive_path = result.eval_dir / "rules_positive.sarif"
    diff_path = result.eval_dir.parent / "prediction.diff"

    # Check if all required files exist
    if not sarif_negative_path.exists():
        return None
    if not sarif_positive_path.exists():
        return None
    if not diff_path.exists() or diff_path.stat().st_size > 1_000_000_000:
        print(f"  Warning: Skipping precision calculation for {instance.display_path}/{result.agent_config.id} due to missing or too large diff file.")
        return None

    try:
        metrics = calculate_precision(
            sarif_negative_path,
            sarif_positive_path,
            diff_path,
        )

        return InstanceAgentPrecision(
            instance=instance.display_path,
            agent=result.agent_config.id,
            metrics=metrics,
        )
    except Exception as e:
        print(f"  Warning: Failed to calculate precision for {instance.display_path}/{result.agent_config.id}: {e}")
        return None
