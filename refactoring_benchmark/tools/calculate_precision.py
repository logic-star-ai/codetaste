#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path
from typing import Optional

from refactoring_benchmark.coverage.models import SARIFOpengrep, PrecisionMetrics, InstanceAgentPrecision
from refactoring_benchmark.coverage.parse import parse_diff, parse_sarif
from refactoring_benchmark.utils.models import InstanceRow


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
    lines_removed, lines_added = parse_diff(
        diff_content,
        "base",
        "predicted"
    )

    # Create PrecisionMetrics object
    metrics = PrecisionMetrics(
        lines_added=lines_added,
        lines_removed=lines_removed,
        lines_matched_by_addition_rules=lines_matched_by_addition_rules,
        lines_matched_by_removal_rules=lines_matched_by_removal_rules,
    )

    print(f"{diff_path.parent.name}/{diff_path.parent.parent.name} : Total lines added in diff: {len(lines_added):4} lines. Total lines in positive SARIF: {len(lines_matched_by_addition_rules):4} lines.")

    # Compact Debug output
    if debug and (metrics.relevant_removed_lines or metrics.relevant_added_lines):
        print(f"\n  DEBUG: Intersection details for {diff_path.parent.name}/{diff_path.parent.parent.name}")
        for label, intersection, sarif_src, diff_src in [
            ("NEGATIVE MATCHES", metrics.relevant_removed_lines, lines_matched_by_removal_rules, lines_removed),
            ("POSITIVE MATCHES", metrics.relevant_added_lines, lines_matched_by_addition_rules, lines_added)
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

    return metrics


def calculate_for_instance_agent(
    instance: InstanceRow,
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


def main():
    parser = argparse.ArgumentParser(
        description="Calculate line-level precision metrics for refactoring changes across instances and agents.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path(__file__).parent.parent.parent / "instances.csv",
        help="Path to instances CSV file",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "output",
        help="Base directory containing agent outputs",
    )

    parser.add_argument(
        "--agent",
        action="append",
        dest="agents",
        required=True,
        help="Agent name to calculate precision for (can be specified multiple times, e.g., --agent golden_agent --agent claude-code)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print detailed debug information about line matches between SARIF and diff",
    )

    args = parser.parse_args()

    # Resolve paths
    instances_csv = args.instances_csv.resolve()
    output_dir = args.output_dir.resolve()

    # Validate instances CSV exists
    if not instances_csv.exists():
        print(f"Error: instances.csv not found at {instances_csv}")
        return 1

    # Load instances
    print(f"Loading instances from {instances_csv}...")
    instances = []
    try:
        with open(instances_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                instances.append(InstanceRow(**row))
    except Exception as e:
        print(f"Error: Failed to load instances from CSV: {e}")
        return 1

    if not instances:
        print("Warning: No instances found in CSV")
        return 0

    # Validate null_agent exists (required for baseline negative SARIF)
    null_agent_instances = 0
    for instance in instances:
        null_agent_dir = output_dir / instance.owner / instance.repo / instance.short_hash / "null_agent"
        if null_agent_dir.exists():
            null_agent_instances += 1

    if null_agent_instances == 0:
        print("Error: null_agent not found for any instances. Precision of deletions requires null_agent baseline.")
        print("Run: python -m refactoring_benchmark.tools.create_pseudo_agents --agent null")
        return 1

    if null_agent_instances < len(instances):
        print(f"Warning: null_agent found for only {null_agent_instances}/{len(instances)} instances")
        print("Some instances will be skipped.")
        print()

    print(f"Loaded {len(instances)} instances")
    print(f"Calculating precision metrics for agents: {', '.join(args.agents)}")
    print(f"Output directory: {output_dir}")
    print(f"Using null_agent baseline for precision of deletions")
    print()

    # Calculate precision for all instance-agent pairs
    results: list[InstanceAgentPrecision] = []
    for agent_name in args.agents:
        print(f"Processing agent: {agent_name}")
        for instance in instances:
            result = calculate_for_instance_agent(instance, agent_name, output_dir, debug=args.debug)
            if result:
                results.append(result)
                print(f"  ✓ {instance.display_path}: added={result.metrics.precision_added:.4f} removed={result.metrics.precision_removed:.4f} overall={result.metrics.precision_overall:.4f}")
            # Silently skip instances without files
        print()

    # Aggregate results by agent
    print("=" * 60)
    print("AGGREGATE RESULTS")
    print("=" * 60)
    print()

    for agent_name in args.agents:
        agent_results = [r for r in results if r.agent == agent_name]

        if not agent_results:
            print(f"{agent_name}:")
            print(f"  No results (missing files for all instances)")
            print()
            continue

        # Calculate statistics for each metric
        precision_added_scores = [r.metrics.precision_added for r in agent_results]
        precision_removed_scores = [r.metrics.precision_removed for r in agent_results]
        precision_overall_scores = [r.metrics.precision_overall for r in agent_results]

        print(f"{agent_name}:")
        print(f"  Instances: {len(agent_results)}/{len(instances)}")
        print()
        print(f"  Precision of Additions: 'Of all the new lines the agent added, how many match the 'good' patterns we expected?'")
        print(f"    (+ lines in {agent_name}/prediction.diff ∩ + lines matched by {agent_name}/rules_positive.sarif)")
        print(f"    ────────────────────────────────────────────────────────────────────────────")
        print(f"    (total + lines in {agent_name}/prediction.diff)")
        print()
        print(f"    Average: {sum(precision_added_scores) / len(precision_added_scores):.4f}")
        print(f"    Min: {min(precision_added_scores):.4f}")
        print(f"    Max: {max(precision_added_scores):.4f}")
        print()
        print(f"  Precision of Deletions: 'Of all the lines the agent decided to delete, how many were actually 'bad' code?'")
        print(f"    (- lines in {agent_name}/prediction.diff ∩ - lines matched by null_agent/rules_negative.sarif)")
        print(f"    ────────────────────────────────────────────────────────────────────────────")
        print(f"    (total - lines in {agent_name}/prediction.diff)")
        print()
        print(f"    Average: {sum(precision_removed_scores) / len(precision_removed_scores):.4f}")
        print(f"    Min: {min(precision_removed_scores):.4f}")
        print(f"    Max: {max(precision_removed_scores):.4f}")
        print()
        print(f"  Overall Precision (all changed lines):")
        print(f"    (unique lines from both intersections)")
        print(f"    ────────────────────────────────────────────────────────────────────────────")
        print(f"    (total changed lines: - lines + + lines)")
        print()
        print(f"    Average: {sum(precision_overall_scores) / len(precision_overall_scores):.4f}")
        print(f"    Min: {min(precision_overall_scores):.4f}")
        print(f"    Max: {max(precision_overall_scores):.4f}")
        print()

        # Create histogram of overall precision
        print(f"  Overall Precision Distribution (histogram):")
        buckets = [0] * 10  # 10 buckets: [0.0, 0.1), [0.1, 0.2), ..., [0.9, 1.0]

        for score in precision_overall_scores:
            bucket_idx = min(int(score * 10), 9)  # Map to bucket index, cap at 9 for score=1.0
            buckets[bucket_idx] += 1

        max_count = max(buckets) if buckets else 1
        bar_width = 40  # Max width of bars

        for i, count in enumerate(buckets):
            bucket_start = i / 10
            bucket_end = (i + 1) / 10
            bar_length = int((count / max_count) * bar_width) if max_count > 0 else 0
            bar = "█" * bar_length
            print(f"    [{bucket_start:.1f}, {bucket_end:.1f}): {bar} {count}")
        print()

    return 0


if __name__ == "__main__":
    exit(main())
