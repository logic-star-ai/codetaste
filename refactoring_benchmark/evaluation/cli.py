"""Command-line interface for evaluation script."""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for evaluation execution.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Evaluate inference results using test and rule-based metrics.",
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
        "--agent-id",
        type=str,
        required=True,
        help="Agent ID to evaluate (must match directory name in output)",
    )

    parser.add_argument(
        "--nr-workers",
        type=int,
        default=4,
        help="Number of parallel workers (threads) for evaluation",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./output"),
        help="Base directory for inference outputs",
    )

    parser.add_argument(
        "--timeout-test",
        type=int,
        default=1200,
        help="Timeout in seconds for test evaluation (default: 20 minutes)",
    )

    parser.add_argument(
        "--timeout-rule",
        type=int,
        default=1200,
        help="Timeout in seconds for rule evaluation (default: 20 minutes)",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-evaluation even if results already exist",
    )

    parser.add_argument(
        "--retry-null-tests",
        action="store_true",
        help="Retry evaluation for instances where test metrics are null (e.g., due to timeouts or crashes)",
    )

    parser.add_argument(
        "--create-rule-report",
        action="store_true",
        help="Create detailed rule evaluation report files",
    )
    
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip test evaluation and only run rule evaluation",
    )

    args = parser.parse_args()

    # Convert paths to absolute
    args.instances_csv = args.instances_csv.resolve()
    args.output_dir = args.output_dir.resolve()

    return args
