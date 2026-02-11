#!/usr/bin/env python3
"""Compute and print precision metrics per instance for a given output directory."""

import argparse
from pathlib import Path
from typing import Optional, Tuple

from refactoring_benchmark.coverage.precision import calculate_precision
from refactoring_benchmark.utils.common import load_instances_from_csv
from refactoring_benchmark.utils.models import ReducedInstanceRow


def _resolve_agent_dir(instance_dir: Path, agent: Optional[str]) -> Tuple[Optional[Path], Optional[str], Optional[str]]:
    if agent:
        return instance_dir / agent, agent, None

    # Agent-less layout: output_dir/{owner}/{repo}/{short_hash}/prediction.diff
    direct_diff = instance_dir / "prediction.diff"
    direct_eval = instance_dir / "evaluation" / "rules_positive.sarif"
    if direct_diff.exists() and direct_eval.exists():
        return instance_dir, instance_dir.name, None

    # Standard layout: output_dir/{owner}/{repo}/{short_hash}/{agent}/prediction.diff
    candidates = []
    if instance_dir.exists():
        for child in instance_dir.iterdir():
            if not child.is_dir():
                continue
            if (child / "prediction.diff").exists() and (child / "evaluation" / "rules_positive.sarif").exists():
                candidates.append(child)

    if len(candidates) == 1:
        return candidates[0], candidates[0].name, None
    if len(candidates) == 0:
        return None, None, "no_agent_dir"
    return None, None, "multiple_agents"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compute and print precision for each instance in instances.csv.",
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
        default=Path(__file__).parent.parent.parent / "outputs" / "instructed" / "direct",
        help="Base directory containing agent outputs",
    )
    parser.add_argument(
        "--null-agent-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "outputs" / "pseudo_agents" / "direct",
        help="Base directory containing null_agent outputs for precision baseline",
    )
    parser.add_argument(
        "--agent",
        type=str,
        default=None,
        help="Agent name to calculate precision for. If omitted, attempt to infer a single agent per instance.",
    )
    parser.add_argument(
        "--quiet-missing",
        action="store_true",
        help="Suppress warnings for instances missing required files.",
    )

    args = parser.parse_args()
    instances_csv = args.instances_csv.resolve()
    output_dir = args.output_dir.resolve()
    null_agent_dir = args.null_agent_dir.resolve()

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
        print("Warning: no instances found in CSV")
        return 0

    print(f"Loaded {len(instances)} instances from {instances_csv}")
    print(f"Output directory: {output_dir}")
    print(f"Null agent directory: {null_agent_dir}")
    if args.agent:
        print(f"Agent: {args.agent}")
    print()

    for instance in instances:
        instance_dir = output_dir / instance.owner / instance.repo / instance.short_hash
        agent_dir, agent_label, agent_error = _resolve_agent_dir(instance_dir, args.agent)

        if agent_dir is None:
            if not args.quiet_missing:
                if agent_error == "multiple_agents":
                    print(f"- {instance.display_path}: skipped (multiple agents found; pass --agent)")
                else:
                    print(f"- {instance.display_path}: skipped (no agent outputs found)")
            continue

        null_agent_instance_dir = null_agent_dir / instance.owner / instance.repo / instance.short_hash / "null_agent"
        sarif_negative_path = null_agent_instance_dir / "evaluation" / "rules_negative.sarif"
        sarif_positive_path = agent_dir / "evaluation" / "rules_positive.sarif"
        diff_path = agent_dir / "prediction.diff"

        missing = []
        if not sarif_negative_path.exists():
            missing.append(f"{null_agent_dir}/evaluation/rules_negative.sarif")
        if not sarif_positive_path.exists():
            missing.append(f"{agent_dir}/evaluation/rules_positive.sarif")
        if not diff_path.exists():
            missing.append(f"{agent_dir}/prediction.diff")

        if missing:
            if not args.quiet_missing:
                missing_str = ", ".join(missing)
                print(f"- {instance.display_path}: skipped (missing {missing_str})")
            continue

        try:
            metrics = calculate_precision(
                sarif_negative_path=sarif_negative_path,
                sarif_positive_path=sarif_positive_path,
                diff_path=diff_path,
            )
        except Exception as exc:
            if not args.quiet_missing:
                print(f"- {instance.display_path}: failed ({exc})")
            continue

        print(
            f"- {instance.display_path} [{agent_label}]: "
            f"added={metrics.precision_added:.4f} "
            f"removed={metrics.precision_removed:.4f} "
            f"overall={metrics.precision_overall:.4f}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
