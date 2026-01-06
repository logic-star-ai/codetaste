"""Main entry point for running inference on benchmark instances."""

import csv
import sys
from pathlib import Path

from refactoring_benchmark.inference.cli import parse_args
from refactoring_benchmark.inference.executor import InferenceOrchestrator
from refactoring_benchmark.inference.models import InferenceConfig
from refactoring_benchmark.inference.validation import (
    sanitize_agent_id,
    validate_agent_config,
    validate_agent_dir,
)
from refactoring_benchmark.utils.logger import get_logger, setup_logging
from refactoring_benchmark.utils.models import InstanceRow


def main():
    """Main entry point for the inference script."""
    # Parse command-line arguments
    args = parse_args()

    # Setup logging
    log_dir = Path("logs") / "inference"
    log_dir.mkdir(parents=True, exist_ok=True)
    setup_logging(str(log_dir))
    logger = get_logger("inference")

    logger.info("=" * 60)
    logger.info("Starting Inference Execution")
    logger.info("=" * 60)

    # Validate agent directory
    try:
        validate_agent_dir(args.agent_dir)
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Invalid agent directory: {e}")
        sys.exit(1)

    # Load and validate agent configuration
    try:
        agent_config_path = args.agent_dir / "agent_config.json"
        agent_config = validate_agent_config(agent_config_path)
        logger.info(f"Loaded agent config: {agent_config.id}")
        logger.info(f"  Agent: {agent_config.agent.name} ({agent_config.agent.provider})")
        logger.info(f"  Model: {agent_config.model.name} ({agent_config.model.provider})")
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Invalid agent configuration: {e}")
        sys.exit(1)

    # Sanitize agent ID for filesystem use
    try:
        sanitized_agent_id = sanitize_agent_id(agent_config.id)
        if sanitized_agent_id != agent_config.id:
            logger.info(f"Sanitized agent ID: '{agent_config.id}' -> '{sanitized_agent_id}'")
    except ValueError as e:
        logger.error(f"Invalid agent ID: {e}")
        sys.exit(1)

    # Load instances from CSV
    if not args.instances_csv.exists():
        logger.error(f"Instances CSV not found: {args.instances_csv}")
        sys.exit(1)

    instances = []
    try:
        with open(args.instances_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                instances.append(InstanceRow(**row))
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
        logger.info(f"Running inference on first {len(instances_to_run)} instances (--instances={args.instances})")
    else:
        logger.info(f"Running inference on all {len(instances_to_run)} instances")

    # Create inference configuration
    inference_config = InferenceConfig(
        agent_dir=args.agent_dir,
        output_dir=args.output_dir,
        instances_csv=args.instances_csv,
        nr_workers=args.nr_workers,
        timeout=args.timeout,
        instances_limit=args.instances,
        force=args.force,
        agent_config=agent_config,
        sanitized_agent_id=sanitized_agent_id,
        env_vars=args.env_vars,
        description_type=args.description_type,
    )

    # Create and run orchestrator
    orchestrator = InferenceOrchestrator(instances_to_run, inference_config)
    orchestrator.run()


if __name__ == "__main__":
    main()
