#!/usr/bin/env python3
import argparse
from pathlib import Path

from refactoring_benchmark.coverage.models import InstanceAgentPrecision
from refactoring_benchmark.coverage.precision import calculate_precision_instance_agent
from refactoring_benchmark.utils.common import load_instances_from_csv
from refactoring_benchmark.utils.models import ReducedInstanceRow


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
    try:
        instances = load_instances_from_csv(instances_csv)
        instances = [ReducedInstanceRow(**instance.model_dump()) for instance in instances]
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
            result = calculate_precision_instance_agent(instance, agent_name, output_dir, debug=args.debug)
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
