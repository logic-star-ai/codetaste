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
        help="Path to the agent directory containing setup_agent.sh, run_agent, and agent_config.json",
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
        default=3600,
        help="Timeout in seconds for each instance inference",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-run inference even if outputs already exist",
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
        choices=["standard", "minimal", "open", "nano"],
        default="standard",
        help="Type of task description to use (standard: full description, minimal: title and summary only, open: open-ended refactoring prompt, nano: very brief description)",
    )

    args = parser.parse_args()

    # Convert paths to absolute
    if args.output_dir is None:
        if args.description_type == "standard":
            args.output_dir = Path("./output")
        elif args.description_type == "minimal":
            args.output_dir = Path("./output_minimal")
        elif args.description_type == "open":
            args.output_dir = Path("./output_open")
        elif args.description_type == "nano":
            args.output_dir = Path("./output_nano")
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
