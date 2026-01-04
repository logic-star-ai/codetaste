"""Command-line interface for bootstrap."""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for bootstrap execution."""
    parser = argparse.ArgumentParser(description="Bootstrap benchmark instances")

    parser.add_argument(
        "--instances",
        type=int,
        default=10,
        help="Number of instances to bootstrap (default: 10)",
    )

    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path("./instances.csv"),
        help="Path to instances CSV file (default: ./instances.csv)",
    )

    parser.add_argument(
        "--nr-workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)",
    )

    parser.add_argument(
        "--force-runtime-build",
        action="store_true",
        help="Force rebuild of runtime images even if they exist",
    )

    return parser.parse_args()
