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
        default=Path("./output"),
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

    args = parser.parse_args()

    # Convert paths to absolute
    args.agent_dir = args.agent_dir.resolve()
    args.output_dir = args.output_dir.resolve()
    args.instances_csv = args.instances_csv.resolve()

    return args
