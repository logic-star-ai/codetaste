"""Calculate line-level precision metrics for refactoring changes."""

import json
import os
from pathlib import Path
from typing import Optional

from refactoring_benchmark.coverage.models import (
    SARIFOpengrep,
    PrecisionMetrics,
    InstanceAgentPrecision,
)
from refactoring_benchmark.coverage.parse import parse_diff, parse_sarif
from refactoring_benchmark.evaluation.models import EvaluationResult
from refactoring_benchmark.utils.models import ReducedInstanceRow
from joblib import Memory

cachedir = './.cache_dir'
memory = Memory(cachedir, verbose=1)

def _debug_print_line_intersections(
    metrics: PrecisionMetrics,
    lines_matched_by_removal_rules: set,
    lines_removed: set,
    lines_matched_by_addition_rules: set,
    lines_added: set,
    diff_path: Path,
) -> None:
    """Print debug information about line intersections between SARIF and diff.

    Args:
        metrics: PrecisionMetrics object with intersection data
        lines_matched_by_removal_rules: Lines matched by negative SARIF rules
        lines_removed: Lines removed in the diff
        lines_matched_by_addition_rules: Lines matched by positive SARIF rules
        lines_added: Lines added in the diff
        diff_path: Path to the diff file (for display purposes)
    """
    if not (metrics.relevant_removed_lines or metrics.relevant_added_lines):
        return

    print(f"\n  DEBUG: Intersection details for {diff_path.parent.name}/{diff_path.parent.parent.name}")

    for label, intersection, sarif_src, diff_src in [
        (
            "NEGATIVE MATCHES",
            metrics.relevant_removed_lines,
            lines_matched_by_removal_rules,
            lines_removed,
        ),
        (
            "POSITIVE MATCHES",
            metrics.relevant_added_lines,
            lines_matched_by_addition_rules,
            lines_added,
        ),
    ]:
        if not intersection:
            continue

        print(f"\n  {label} ({len(intersection)} lines):")
        # Speed up lookups with a dictionary
        s_map = {(l.uri, l.line_number): l for l in sarif_src}
        d_map = {(l.uri, l.line_number): l for l in diff_src}

        for line in sorted(intersection, key=lambda x: (x.uri, x.line_number))[:5]:
            s_line, d_line = s_map.get((line.uri, line.line_number)), d_map.get((line.uri, line.line_number))
            s_cont = s_line.content.strip() if s_line and s_line.content else ""
            d_cont = d_line.content.strip() if d_line and d_line.content else ""
            match = "✓" if (s_cont and d_cont and (s_cont in d_line.content or d_cont in s_line.content)) else "✗"
            print(f"    {match} {line.uri}:{line.line_number}")
            print(f"      SARIF: {repr(s_cont[:70]) if s_cont else '<no content>'}")
            print(f"      DIFF:  {repr(d_cont[:70]) if d_cont else '<no content>'}")

    print()


def calculate_precision(
    sarif_negative_path: Path,
    sarif_positive_path: Path,
    diff_path: Path,
    debug: bool = False,
) -> PrecisionMetrics:
    paths = [sarif_negative_path, sarif_positive_path, diff_path]
    mtimes = tuple(os.path.getmtime(p) for p in paths)
    return _cached_calculate_precision(
        sarif_negative_path, sarif_positive_path, diff_path, mtimes, debug
    )

@memory.cache
def _cached_calculate_precision(
    sarif_negative_path: Path,
    sarif_positive_path: Path,
    diff_path: Path,
    mtimes: tuple,
    debug: bool = False,
) -> PrecisionMetrics:
    """
    Calculate line-level precision metrics for refactoring changes.

    Args:
        sarif_negative_path: Path to rules_negative.sarif (negative rules on base code)
        sarif_positive_path: Path to rules_positive.sarif (positive rules on predicted code)
        diff_path: Path to prediction.diff
        debug: Whether to print debug information

    Returns:
        PrecisionMetrics object with precision scores and line sets
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

    # Create PrecisionMetrics object
    metrics = PrecisionMetrics(
        lines_added=lines_added,
        lines_removed=lines_removed,
        lines_matched_by_addition_rules=lines_matched_by_addition_rules,
        lines_matched_by_removal_rules=lines_matched_by_removal_rules,
    )

    # Print debug output if requested
    if debug:
        print(
            (
                f"{diff_path.parent.name}/{diff_path.parent.parent.name} : Total lines added in diff: {len(lines_added):4} lines. "
                f"Total lines in positive SARIF: {len(lines_matched_by_addition_rules):4} lines."
            )
        )
        _debug_print_line_intersections(
            metrics,
            lines_matched_by_removal_rules,
            lines_removed,
            lines_matched_by_addition_rules,
            lines_added,
            diff_path,
        )

    return metrics


def calculate_precision_eval_result(
    result: EvaluationResult,
    null_agent_dir: Path = Path("output_pseudo_agents"),
    debug: bool = False,
) -> Optional[InstanceAgentPrecision]:
    """
    Calculate precision metrics for a single instance-agent pair.

    Uses baseline negative SARIF from null_agent (shared across all agents)
    and agent-specific positive SARIF.

    Args:
        result: EvaluationResult object
        null_agent_dir: Directory containing pseudo agents
        debug: Whether to print debug information

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
    if not diff_path.exists() or diff_path.stat().st_size > 10_000_000:
        print(f"  Warning: Skipping precision calculation for {instance.display_path}/{result.agent_config.id} due to missing or too large diff file.")
        return None

    try:
        metrics = calculate_precision(
            sarif_negative_path,
            sarif_positive_path,
            diff_path,
            debug=debug,
        )

        return InstanceAgentPrecision(
            instance=instance.display_path,
            agent=result.agent_config.id,
            metrics=metrics,
        )
    except Exception as e:
        print(f"  Warning: Failed to calculate precision for {instance.display_path}/{result.agent_config.id}: {e}")
        return None
