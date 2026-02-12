#!/usr/bin/env python3
"""Compute average max(0, negative_ifr - positive_ifr) across instances."""

import argparse
from pathlib import Path
from typing import Optional, Tuple

from refactoring_benchmark.evaluation.models import EvaluationResult
from refactoring_benchmark.utils.common import load_instances_from_csv
from refactoring_benchmark.utils.models import ReducedInstanceRow


def _resolve_agent_dir(instance_dir: Path, agent: Optional[str]) -> Tuple[Path, str]:
    if agent:
        return instance_dir / agent, agent

    direct_eval = instance_dir / "evaluation" / "evaluation_result.json"
    if direct_eval.exists():
        return instance_dir, instance_dir.name

    candidates = []
    if instance_dir.exists():
        for child in instance_dir.iterdir():
            if not child.is_dir():
                continue
            if (child / "evaluation" / "evaluation_result.json").exists():
                candidates.append(child)

    if len(candidates) == 1:
        return candidates[0], candidates[0].name
    if len(candidates) == 0:
        raise FileNotFoundError(f"No agent outputs found in {instance_dir}")
    raise ValueError(f"Multiple agents found in {instance_dir}; pass --agent")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compute average pos_rule_bias across instances.",
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
        "--agent",
        type=str,
        default=None,
        help="Agent name to calculate pos_rule_bias for. If omitted, attempt to infer a single agent per instance.",
    )

    args = parser.parse_args()
    instances_csv = args.instances_csv.resolve()
    output_dir = args.output_dir.resolve()

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
    print(f"Output directory: {output_dir}")
    if args.agent:
        print(f"Agent: {args.agent}")
    print()

    total = 0.0
    count = 0
    # claude-code-v2.0.76-sonnet45  codex-v0.77.0-gpt-5.1-codex-mini  codex-v0.77.0-gpt-5.2  golden_agent  null_agent  qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct
    agent_ids = (
        [args.agent]
        if args.agent
        else [
            "claude-code-v2.0.76-sonnet45",
            "codex-v0.77.0-gpt-5.1-codex-mini",
            "codex-v0.77.0-gpt-5.2",
            "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct",
        ]
    )
    for agent_id in agent_ids:
        for instance in instances:
            instance_dir = output_dir / instance.owner / instance.repo / instance.short_hash
            try:
                agent_dir, agent_label = _resolve_agent_dir(instance_dir, agent_id)
            except Exception as exc:
                print(f"Error: {instance.display_path}: {exc}")
                return 1

            eval_path = agent_dir / "evaluation" / "evaluation_result.json"
            if not eval_path.exists():
                print(f"Error: {instance.display_path}: missing {eval_path}")
                return 1

            try:
                result = EvaluationResult.load_from_json(eval_path)
            except Exception as exc:
                print(f"Error: {instance.display_path}: failed to load {eval_path}: {exc}")
                return 1

            metrics = result.agent_rule_metrics
            bias = max(0.0, metrics.negative_ifr - metrics.positive_ifr)
            print(
                f"{instance.display_path} ({agent_label}): pos_rule_bias={bias:.4f} (negative_ifr={metrics.negative_ifr:.4f}, positive_ifr={metrics.positive_ifr:.4f})"
            )
            total += bias
            count += 1

    avg = total / count if count else 0.0
    print(
        f"pos_rule_bias average: {avg:.6f} ({count // len(agent_ids)} instances * {len(agent_ids)} agents) High means biased. Initially ~0.15 on multiplan ; ~0.08 on instructed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
