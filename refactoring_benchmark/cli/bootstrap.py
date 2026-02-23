"""Main entry point for bootstrap execution."""

import os
import sys
from pathlib import Path

from refactoring_benchmark.bootstrap.cli import parse_args
from refactoring_benchmark.bootstrap.executor import BootstrapOrchestrator
from refactoring_benchmark.bootstrap.models import BootstrapConfig
from refactoring_benchmark.utils.common import load_instances_from_csv
from refactoring_benchmark.utils.logger import get_logger, setup_logging


def main():
    """Main entry point for bootstrap."""
    # Parse arguments
    args = parse_args()

    # Setup logging
    log_dir = Path("logs/bootstrap")
    setup_logging(log_dir)
    logger = get_logger("bootstrap")

    # Validate API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("Missing ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    # Validate instances CSV
    if not args.instances_csv.exists():
        logger.error(f"Instances CSV not found: {args.instances_csv}")
        sys.exit(1)

    # Load instances
    try:
        instances = load_instances_from_csv(args.instances_csv)
    except Exception as e:
        logger.error(f"Failed to load instances: {e}")
        sys.exit(1)

    if not instances:
        logger.error("No instances found in CSV")
        sys.exit(1)

    # Limit to requested number
    instances = instances[: args.instances]
    logger.info(f"Loaded {len(instances)} instances from {args.instances_csv}")

    # Create configuration
    config = BootstrapConfig(
        instances_csv=args.instances_csv,
        nr_workers=args.nr_workers,
        force_runtime_build=args.force_runtime_build,
        rerun_metrics=args.rerun_metrics,
        force_full_build=args.force_full_build,
        api_key=api_key,
    )

    # Run bootstrap
    orchestrator = BootstrapOrchestrator(instances, config)
    orchestrator.run()


if __name__ == "__main__":
    main()
