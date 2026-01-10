"""Calculate line-level precision metrics for refactoring changes."""

import json
from pathlib import Path
from typing import Optional

from refactoring_benchmark.coverage.models import (
    SARIFOpengrep,
    PrecisionMetrics,
    InstanceAgentPrecision,
)
from refactoring_benchmark.coverage.parse import parse_diff, parse_sarif
from refactoring_benchmark.utils.models import ReducedInstanceRow


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
    diff_content = diff_path.read_text()
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


def calculate_precision_instance_agent(
    instance: ReducedInstanceRow,
    agent_name: str,
    output_dir: Path,
    debug: bool = False,
) -> Optional[InstanceAgentPrecision]:
    """
    Calculate precision metrics for a single instance-agent pair.

    Uses baseline negative SARIF from null_agent (shared across all agents)
    and agent-specific positive SARIF.

    Args:
        instance: Instance row from CSV
        agent_name: Name of the agent
        output_dir: Base output directory
        debug: Whether to print debug information

    Returns:
        InstanceAgentPrecision object with results, or None if files don't exist or calculation fails
    """
    # Construct paths
    instance_dir = output_dir / instance.owner / instance.repo / instance.short_hash
    instance_agent_dir = instance_dir / agent_name
    eval_dir = instance_agent_dir / "evaluation"

    # Use null_agent for baseline negative SARIF (bad patterns in base code)
    null_agent_dir = instance_dir / "null_agent"
    sarif_negative_path = null_agent_dir / "evaluation" / "rules_negative.sarif"

    # Use agent-specific positive SARIF (good patterns in agent's solution)
    sarif_positive_path = eval_dir / "rules_positive.sarif"
    diff_path = instance_agent_dir / "prediction.diff"

    # Check if all required files exist
    if not sarif_negative_path.exists():
        return None
    if not sarif_positive_path.exists():
        return None
    if not diff_path.exists():
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
            agent=agent_name,
            metrics=metrics,
        )
    except Exception as e:
        print(f"  Warning: Failed to calculate precision for {instance.display_path}/{agent_name}: {e}")
        return None
