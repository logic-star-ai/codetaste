"""Main entry point for evaluating inference results."""

import sys
from pathlib import Path

from refactoring_benchmark.evaluation.cli import parse_args
from refactoring_benchmark.evaluation.executor import EvaluationOrchestrator
from refactoring_benchmark.evaluation.models import EvaluationConfig
from refactoring_benchmark.utils.common import load_instances_from_csv
from refactoring_benchmark.utils.logger import get_logger, setup_logging


def main():
    """Main entry point for the evaluation script."""
    # Parse command-line arguments
    args = parse_args()

    # Setup logging
    log_dir = Path("logs") / "evaluation"
    log_dir.mkdir(parents=True, exist_ok=True)
    setup_logging(str(log_dir))
    logger = get_logger("evaluation")

    logger.info("=" * 60)
    logger.info("Starting Evaluation Execution")
    logger.info("=" * 60)

    # Load instances from CSV
    if not args.instances_csv.exists():
        logger.error(f"Instances CSV not found: {args.instances_csv}")
        sys.exit(1)

    try:
        instances = load_instances_from_csv(args.instances_csv)
    except Exception as e:
        logger.error(f"Failed to load instances from CSV: {e}")
        sys.exit(1)

    if not instances:
        logger.warning("No instances found in CSV")
        sys.exit(0)

    logger.info(f"Loaded {len(instances)} instances from {args.instances_csv}")

    # Select subset of instances based on --instances flag
    instances_to_run = instances[: args.instances]
    if len(instances_to_run) < len(instances):
        logger.info(f"Evaluating first {len(instances_to_run)} instances (--instances={args.instances})")
    else:
        logger.info(f"Evaluating all {len(instances_to_run)} instances")

    logger.info(f"Agent ID: {args.agent_id}")

    # Create evaluation configuration
    eval_config = EvaluationConfig(
        instances_csv=args.instances_csv,
        agent_id=args.agent_id,
        output_dir=args.output_dir,
        nr_workers=args.nr_workers,
        timeout_test=args.timeout_test,
        timeout_rule=args.timeout_rule,
        force=args.force,
        retry_null_tests=args.retry_null_tests,
        create_rule_report=args.create_rule_report,
        skip_tests=args.skip_tests,
    )

    # Create and run orchestrator
    orchestrator = EvaluationOrchestrator(instances_to_run, args.agent_id, eval_config)
    orchestrator.run()


if __name__ == "__main__":
    main()
