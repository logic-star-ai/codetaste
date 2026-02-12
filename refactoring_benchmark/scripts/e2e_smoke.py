"""Run a small end-to-end pipeline: inference -> evaluation -> analysis. (Smoke Test)"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

from refactoring_benchmark.inference.validation import sanitize_agent_id
from refactoring_benchmark.utils.common import load_instances_from_csv


DEFAULT_AGENT_DIR = Path("./agents/qwen-code/qwen3-coder-30b-a3b-instruct")
DEFAULT_DESCRIPTION_TYPES = ["instructed", "open"]
DEFAULT_MODES = ["direct", "plan", "multiplan"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run inference, evaluation, and analysis for a small E2E slice.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--instances", type=int, default=2, help="Number of instances to run")
    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path("./instances.csv"),
        help="Path to instances CSV",
    )
    parser.add_argument(
        "--agent-dir",
        type=Path,
        default=DEFAULT_AGENT_DIR,
        help="Agent directory containing agent_config.json",
    )
    parser.add_argument(
        "--description-type",
        action="append",
        dest="description_types",
        choices=DEFAULT_DESCRIPTION_TYPES,
        help="Description types to run (can be repeated)",
    )
    parser.add_argument(
        "--mode",
        action="append",
        dest="modes",
        choices=DEFAULT_MODES,
        help="Inference modes to run (can be repeated)",
    )
    parser.add_argument("--nr-workers", type=int, default=2, help="Parallel workers")
    parser.add_argument("--timeout", type=int, default=5400, help="Inference timeout per instance")
    parser.add_argument("--plan-timeout", type=int, default=1800, help="Plan/multiplan timeout")
    parser.add_argument(
        "--eval-timeout-test",
        type=int,
        default=1200,
        help="Evaluation test timeout per instance",
    )
    parser.add_argument(
        "--eval-timeout-rule",
        type=int,
        default=1200,
        help="Evaluation rule timeout per instance",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("./outputs"),
        help="Root directory for inference outputs",
    )
    parser.add_argument(
        "--plots-dir",
        type=Path,
        default=Path("./analyze_e2e"),
        help="Directory for analysis plots",
    )
    parser.add_argument(
        "--plot-type",
        type=str,
        default="bar",
        choices=["line", "bar", "scatter"],
        help="Plot type for analysis",
    )
    parser.add_argument(
        "--aggregation",
        type=str,
        default="mean",
        choices=["mean", "median"],
        help="Aggregation method for analysis",
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Environment variable passed to inference containers (repeatable)",
    )
    return parser.parse_args()


def print_cmd(cmd: list[str]) -> None:
    quoted = " ".join(shlex.quote(part) for part in cmd)
    print(f"\n$ {quoted}")


def run_cmd(cmd: list[str]) -> None:
    print_cmd(cmd)
    subprocess.run(cmd, check=True)


def parse_env_list(env_list: list[str]) -> list[str]:
    parsed: list[str] = []
    for env_entry in env_list:
        if "=" not in env_entry:
            raise ValueError(f"Invalid --env value '{env_entry}'; expected KEY=VALUE")
        key, _ = env_entry.split("=", 1)
        if not key:
            raise ValueError(f"Invalid --env value '{env_entry}'; key cannot be empty")
        parsed.append(env_entry)
    return parsed


def read_agent_id(agent_dir: Path) -> str:
    config_path = agent_dir / "agent_config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"agent_config.json not found at {config_path}")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    raw = config.get("id")
    if not raw:
        raise ValueError(f"Could not find agent id in {config_path}")
    return sanitize_agent_id(raw)


def ensure_file(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label}: {path}")


def verify_inference_outputs(
    instances, agent_id: str, output_dir: Path, mode: str
) -> None:
    for inst in instances:
        base = output_dir / inst.owner / inst.repo / inst.short_hash / agent_id
        ensure_file(base / "prediction.diff", "prediction.diff")
        ensure_file(base / "inference_metadata.json", "inference_metadata.json")
        ensure_file(base / "agent_config.json", "agent_config.json")

        if mode == "plan":
            ensure_file(base / "refactoring_plan.md", "refactoring_plan.md")
            ensure_file(base / "plan_metadata.json", "plan_metadata.json")
        elif mode == "multiplan":
            plan_dir = base / "refactoring_plans"
            for idx in range(5):
                ensure_file(plan_dir / f"refactoring_plan{idx}.md", f"refactoring_plan{idx}.md")
            ensure_file(base / "multiplan_generation_metadata.json", "multiplan_generation_metadata.json")
            ensure_file(base / "multiplan_metadata.json", "multiplan_metadata.json")


def verify_evaluation_outputs(instances, agent_id: str, output_dir: Path) -> None:
    for inst in instances:
        eval_dir = output_dir / inst.owner / inst.repo / inst.short_hash / agent_id / "evaluation"
        ensure_file(eval_dir / "evaluation_result.json", "evaluation_result.json")
        ensure_file(eval_dir / "rules_positive.sarif", "rules_positive.sarif")
        ensure_file(eval_dir / "rules_negative.sarif", "rules_negative.sarif")
        ensure_file(eval_dir / "test_output.txt", "test_output.txt")
        ensure_file(eval_dir / "rule_output.txt", "rule_output.txt")


def main() -> int:
    args = parse_args()

    instances_csv = args.instances_csv.resolve()
    agent_dir = args.agent_dir.resolve()
    output_root = args.output_root.resolve()
    plots_dir = args.plots_dir.resolve()

    description_types = args.description_types or DEFAULT_DESCRIPTION_TYPES
    modes = args.modes or DEFAULT_MODES
    env_list = parse_env_list(args.env)

    if args.instances < 1:
        raise ValueError("--instances must be >= 1")

    ensure_file(instances_csv, "instances CSV")
    instances = load_instances_from_csv(instances_csv)[: args.instances]
    if not instances:
        raise ValueError("No instances found in the CSV")

    agent_id = read_agent_id(agent_dir)
    print(f"Agent ID: {agent_id}")
    print(f"Instances: {len(instances)} from {instances_csv}")
    print(f"Description types: {', '.join(description_types)}")
    print(f"Modes: {', '.join(modes)}")

    for description_type in description_types:
        for mode in modes:
            output_dir = output_root / description_type / mode
            cmd = [
                sys.executable,
                "-m",
                "refactoring_benchmark.scripts.inference",
                "--instances",
                str(args.instances),
                "--instances-csv",
                str(instances_csv),
                "--agent-dir",
                str(agent_dir),
                "--description-type",
                description_type,
                "--nr-workers",
                str(args.nr_workers),
                "--timeout",
                str(args.timeout),
                "--plan-timeout",
                str(args.plan_timeout),
                "--output-dir",
                str(output_dir),
            ]
            if mode == "plan":
                cmd.append("--plan")
            elif mode == "multiplan":
                cmd.append("--multiplan")
            for env_entry in env_list:
                cmd.extend(["--env", env_entry])

            print(f"\n== Inference: {description_type} / {mode} ==")
            run_cmd(cmd)
            verify_inference_outputs(instances, agent_id, output_dir, mode)

            eval_cmd = [
                sys.executable,
                "-m",
                "refactoring_benchmark.scripts.evaluate",
                "--instances",
                str(args.instances),
                "--instances-csv",
                str(instances_csv),
                "--agent-id",
                agent_id,
                "--nr-workers",
                str(args.nr_workers),
                "--timeout-test",
                str(args.eval_timeout_test),
                "--timeout-rule",
                str(args.eval_timeout_rule),
                "--output-dir",
                str(output_dir),
            ]
            print(f"\n== Evaluation: {description_type} / {mode} ==")
            run_cmd(eval_cmd)
            verify_evaluation_outputs(instances, agent_id, output_dir)

    analysis_cmd = [
        sys.executable,
        "-m",
        "refactoring_benchmark.scripts.analyze",
        "--plots-dir",
        str(plots_dir),
        "--plot-type",
        args.plot_type,
        "--aggregation",
        args.aggregation,
        "--instances-csv",
        str(instances_csv),
    ]
    for mode in modes:
        analysis_cmd.extend(["--output-dir", str(output_root / description_types[0] / mode)])

    print("\n== Analysis ==")
    run_cmd(analysis_cmd)

    expected = [
        plots_dir / f"ifr_{args.plot_type}_{args.aggregation}.pdf",
        plots_dir / f"test_success_{args.plot_type}_{args.aggregation}.pdf",
    ]
    for plot_path in expected:
        ensure_file(plot_path, "analysis plot")

    print("\nE2E pipeline completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
