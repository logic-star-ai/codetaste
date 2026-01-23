"""Command-line interface for inference script."""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for inference execution.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Run inference on benchmark instances using agent scripts.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--instances",
        type=int,
        default=15,
        help="Number of instances to run from the CSV file",
    )

    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path("./instances.csv"),
        help="Path to the instances CSV file",
    )

    parser.add_argument(
        "--nr-workers",
        type=int,
        default=4,
        help="Number of parallel workers (threads) for inference",
    )

    parser.add_argument(
        "--agent-dir",
        type=Path,
        default=Path("./agent"),
        help="Path to the agent directory containing setup_system.sh, run_agent, and agent_config.json",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Base directory for inference outputs",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=5400,
        help="Timeout in seconds for each instance inference",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-run inference even if outputs already exist",
    )

    parser.add_argument(
        "--force-unsuccessful",
        action="store_true",
        help="Force re-run inference for instances that were not successful (finish_reason != 'success')",
    )

    parser.add_argument(
        "--reuse-successful-plan",
        action="store_true",
        help="Reuse existing plan if plan_metadata.json shows success (optimization for --plan mode)",
    )

    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Environment variable to pass to containers (can be specified multiple times)",
    )

    parser.add_argument(
        "--description-type",
        type=str,
        default="standard",
        help="Type of task description to use (standard: full description, minimal: title and summary only, open: open-ended refactoring prompt, nano: very brief description, files: open-ended with key files from golden diff, problem: autonomous problem-solving prompt, or any custom type)",
    )

    parser.add_argument(
        "--plan",
        action="store_true",
        help="Enable two-step inference: first create a plan, then execute it",
    )

    parser.add_argument(
        "--plan-timeout",
        type=int,
        default=1800,
        help="Timeout in seconds for the planning step when --plan is enabled (default: 1800 = 30 minutes)",
    )

    parser.add_argument(
        "--multiplan",
        action="store_true",
        help="Enable multi-plan inference: generate 5 different plans, use LLM to select best, then execute it (mutually exclusive with --plan)",
    )

    args = parser.parse_args()

    # Convert paths to absolute
    if args.output_dir is None:
        if args.description_type == "standard":
            base_name = "output"
        else:
            base_name = f"output_{args.description_type}"
        if args.multiplan:
            args.output_dir = Path(f"./{base_name}_multiplan")
        elif args.plan:
            args.output_dir = Path(f"./{base_name}_plan")
        else:
            args.output_dir = Path(f"./{base_name}")
    args.agent_dir = args.agent_dir.resolve()
    args.output_dir = args.output_dir.resolve()
    args.instances_csv = args.instances_csv.resolve()

    # Parse environment variables from KEY=VALUE format
    env_vars = {}
    for env_str in args.env:
        if "=" not in env_str:
            parser.error(f"Invalid --env format: '{env_str}'. Expected KEY=VALUE")
        key, value = env_str.split("=", 1)
        if not key:
            parser.error(f"Invalid --env format: '{env_str}'. Key cannot be empty")
        env_vars[key] = value
    args.env_vars = env_vars

    return args
