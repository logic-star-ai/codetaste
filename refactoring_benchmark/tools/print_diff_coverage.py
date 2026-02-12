#!/usr/bin/env python3
"""Compute diff coverage using golden diffs and pseudo agents."""

import argparse
from pathlib import Path

from refactoring_benchmark.coverage.precision import calculate_precision
from refactoring_benchmark.utils.common import load_instances_from_csv
from refactoring_benchmark.utils.models import ReducedInstanceRow


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compute coverage of golden diffs using pseudo-agent SARIF.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path(__file__).parent.parent.parent / "instances.csv",
        help="Path to instances CSV file",
    )
    parser.add_argument(
        "--diffs-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "assets" / "diffs",
        help="Base directory containing golden diffs",
    )
    parser.add_argument(
        "--pseudo-agents-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "outputs" / "pseudo_agents" / "direct",
        help="Base directory containing pseudo agent outputs",
    )

    args = parser.parse_args()
    instances_csv = args.instances_csv.resolve()
    diffs_dir = args.diffs_dir.resolve()
    pseudo_agents_dir = args.pseudo_agents_dir.resolve()

    if not instances_csv.exists():
        print(f"Error: instances.csv not found at {instances_csv}")
        return 1

    try:
        instances = load_instances_from_csv(instances_csv)
        instances = [ReducedInstanceRow(**instance.model_dump()) for instance in instances]
    except Exception as exc:
        print(f"Error: failed to load instances from CSV: {exc}")
        return 1

    if not instances:
        print("Error: no instances found in CSV")
        return 1

    print(f"Loaded {len(instances)} instances from {instances_csv}")
    print(f"Diffs directory: {diffs_dir}")
    print(f"Pseudo agents directory: {pseudo_agents_dir}")
    print()

    precision_added_scores = []
    precision_removed_scores = []
    precision_overall_scores = []

    for instance in instances:
        diff_path = diffs_dir / instance.owner / instance.repo / instance.short_hash / "golden.diff"
        pos_sarif_path = (
            pseudo_agents_dir
            / instance.owner
            / instance.repo
            / instance.short_hash
            / "golden_agent"
            / "evaluation"
            / "rules_positive.sarif"
        )
        neg_sarif_path = (
            pseudo_agents_dir
            / instance.owner
            / instance.repo
            / instance.short_hash
            / "null_agent"
            / "evaluation"
            / "rules_negative.sarif"
        )

        missing = [p for p in (diff_path, pos_sarif_path, neg_sarif_path) if not p.exists()]
        if missing:
            missing_str = ", ".join(str(p) for p in missing)
            raise FileNotFoundError(f"Missing required file(s) for {instance.display_path}: {missing_str}")

        metrics = calculate_precision(
            sarif_negative_path=neg_sarif_path,
            sarif_positive_path=pos_sarif_path,
            diff_path=diff_path,
        )

        precision_added_scores.append(metrics.precision_added)
        precision_removed_scores.append(metrics.precision_removed)
        precision_overall_scores.append(metrics.precision_overall)

        print(
            f"- {instance.display_path}: "
            f"added={metrics.precision_added:.4f} "
            f"removed={metrics.precision_removed:.4f} "
            f"overall={metrics.precision_overall:.4f}"
        )

    avg_added = sum(precision_added_scores) / len(precision_added_scores)
    avg_removed = sum(precision_removed_scores) / len(precision_removed_scores)
    avg_overall = sum(precision_overall_scores) / len(precision_overall_scores)

    print()
    print(f"Average added coverage: {avg_added:.4f}")
    print(f"Average removed coverage: {avg_removed:.4f}")
    print(f"Average total coverage: {avg_overall:.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
