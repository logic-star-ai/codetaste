"""Executor for running evaluation on benchmark instances."""

import json
import logging
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import time
from typing import List

from tqdm import tqdm

from refactoring_benchmark.evaluation.models import EvaluationConfig, EvaluationResult
from refactoring_benchmark.evaluation.parser import (
    load_instance_metadata,
    parse_rule_evaluation,
    parse_test_output,
)
from refactoring_benchmark.evaluation.runner import run_rule_evaluation, run_test_evaluation
from refactoring_benchmark.inference.models import AgentConfig
from refactoring_benchmark.inference.validation import validate_agent_config
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.logger import get_logger
from refactoring_benchmark.utils.models import InstanceMetadata, InstanceRow


def get_evaluation_dir(instance: InstanceRow, agent_id: str, output_dir: Path) -> Path:
    """
    Get evaluation directory path for an instance and agent.

    Args:
        instance: Benchmark instance
        agent_id: Agent ID
        output_dir: Base output directory

    Returns:
        Path to evaluation directory
    """
    return output_dir / instance.owner / instance.repo / instance.short_hash / agent_id / "evaluation"


def evaluation_exists(eval_dir: Path) -> bool:
    """
    Check if evaluation results already exist.

    Args:
        eval_dir: Evaluation directory

    Returns:
        True if evaluation_result.json exists
    """
    return (eval_dir / "evaluation_result.json").exists()

def load_metadata(agent_config_path: Path, instance_metadata_path: Path, inference_metadata_path: Path, instance_logger: logging.Logger) -> tuple[AgentConfig, InstanceMetadata, dict]:
    # Load agent config
    try:
        agent_config: AgentConfig = validate_agent_config(agent_config_path)
    except Exception as e:
        instance_logger.error(f"Failed to load agent config: {e}")
        raise e

    # Load instance metadata
    try:
        instance_metadata: InstanceMetadata = load_instance_metadata(instance_metadata_path)
    except Exception as e:
        instance_logger.error(f"Failed to load instance metadata: {e}")
        raise e
    
    inference_metadata = None
    if inference_metadata_path.exists():
        try:
            with inference_metadata_path.open("r", encoding="utf-8") as f:
                inference_metadata = json.load(f)
            instance_logger.info("Loaded inference metadata successfully")
        except Exception as e:
            instance_logger.error(f"Failed to load inference metadata: {e}")

    return agent_config, instance_metadata, inference_metadata

def evaluate_single_instance(instance: InstanceRow, agent_id: str, config: EvaluationConfig) -> bool:
    """
    Evaluate a single instance for a given agent.

    Runs test and rule evaluation in parallel.

    Args:
        instance: Benchmark instance
        agent_id: Agent ID to evaluate
        config: Evaluation configuration

    Returns:
        True if successful, False otherwise
    """
    instance_logger = get_logger(f"{instance.id}", use_file=True, use_stdout=False, log_subdir=f"{agent_id}")

    # Determine paths
    agent_output_dir = config.output_dir / instance.owner / instance.repo / instance.short_hash / agent_id
    eval_dir = agent_output_dir / "evaluation"
    prediction_diff = agent_output_dir / "prediction.diff"
    inference_metadata_path = agent_output_dir / "inference_metadata.json"
    instance_metadata_path = eval_dir / "instance_metadata.json"
    agent_config_path = agent_output_dir / "agent_config.json"

    # Check if prediction.diff exists
    if not prediction_diff.exists():
        instance_logger.warning(f"Skipping {instance.id}, no prediction.diff found at {prediction_diff}")
        return False

    try:
        agent_config, instance_metadata, inference_metadata = load_metadata(agent_config_path, instance_metadata_path, inference_metadata_path, instance_logger)
    except Exception:
        return False

    # Check if evaluation already exists
    evaluation_result = None
    if evaluation_exists(eval_dir):
        try:
            evaluation_result = EvaluationResult.load_from_json(eval_dir / "evaluation_result.json")
        except Exception as e:
            instance_logger.warning(f"Could not load evaluation result: {e}, will retry")
        if evaluation_result is not None:
            if not config.force:
                if not config.retry_null_tests:
                    instance_logger.info(f"Skipping {instance.id}, evaluation already exists")
                    return True
                elif evaluation_result.agent_test_metrics is not None:
                    instance_logger.info(f"Skipping {instance.id}, test metrics exist")
                    return True
                else:
                    instance_logger.info(f"Retrying {instance.id}, test metrics are null")
            else:
                instance_logger.info(f"Force re-evaluation enabled, proceeding with evaluation for {instance.id}")

    # Create evaluation directory
    eval_dir.mkdir(parents=True, exist_ok=True)

    instance_logger.info(f"Starting evaluation for {instance.display_path}")
    instance_logger.info(f"  Agent ID: {agent_id}")
    instance_logger.info(f"  Output: {eval_dir}")

    # Run test and rule evaluation in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Submit both evaluations
        if not config.skip_tests:
            test_future = executor.submit(
                run_test_evaluation, instance, prediction_diff, eval_dir, config.timeout_test, instance_logger
            )

        rule_future = executor.submit(
            run_rule_evaluation, instance, prediction_diff, eval_dir, config.timeout_rule, instance_logger
        )

        # Gather results and write outputs
        rule_success, rule_stdout = rule_future.result()
        (eval_dir / "rule_output.txt").write_text(rule_stdout)
        if not config.skip_tests:
            test_metrics, test_stdout = test_future.result()
            (eval_dir / "test_output.txt").write_text(test_stdout)
            if test_metrics is None:
                test_metrics = parse_test_output(test_stdout)
        else:
            test_metrics = evaluation_result.agent_test_metrics if evaluation_result else None

    # Parse rule metrics from SARIF files
    if not rule_success:
        instance_logger.error(f"Rule evaluation failed: {rule_stdout}")
        return False

    try:
        rule_metrics = parse_rule_evaluation(eval_dir, create_report=config.create_rule_report)
    except Exception as e:
        instance_logger.error(f"Failed to parse rule metrics: {e}")
        return False



    # Create evaluation result
    evaluation_result = EvaluationResult(
        instance_metadata=instance_metadata,
        agent_config=agent_config,
        agent_test_metrics=test_metrics,
        agent_rule_metrics=rule_metrics,
        inference_metadata=inference_metadata,
    )

    # Save evaluation result
    result_path = eval_dir / "evaluation_result.json"
    with open(result_path, "w") as f:
        json.dump(evaluation_result.model_dump(mode="json"), f, indent=2)

    instance_logger.info(f"Evaluation completed successfully")
    instance_logger.info(f"  Test metrics: {test_metrics.model_dump() if test_metrics else 'N/A'}")
    instance_logger.info(
        f"  Rule IFR: {rule_metrics.ifr:.3f} (pos: {rule_metrics.positive_ifr:.3f}, neg: {rule_metrics.negative_ifr:.3f})"
    )
    print(
        f"✅ [{instance.id}] : Rule IFR: {rule_metrics.ifr:.3f} (pos: {rule_metrics.positive_ifr:.3f}, neg: {rule_metrics.negative_ifr:.3f}), Test Metrics: {test_metrics.model_dump() if test_metrics else 'N/A'}"
    )

    return True


class EvaluationOrchestrator:
    """Orchestrates parallel evaluation execution."""

    def __init__(self, instances: List[InstanceRow], agent_id: str, config: EvaluationConfig):
        """
        Initialize orchestrator.

        Args:
            instances: List of instances to evaluate
            agent_id: Agent ID to evaluate
            config: Evaluation configuration
        """
        self.instances = instances
        self.agent_id = agent_id
        self.config = config
        self.logger = get_logger("evaluation")
        self.executor = None

        # Setup signal handlers
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Register signal handlers for graceful shutdown."""

        def signal_handler(signum, frame):
            sig_name = signal.Signals(signum).name
            self.logger.warning(f"\nReceived {sig_name}, initiating shutdown...")
            if self.executor:
                self.executor.shutdown(wait=False, cancel_futures=True)
            self._cleanup_containers()
            print(f"Exiting due to {sig_name}")
            time.sleep(1)
            sys.exit(1)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def _cleanup_containers(self):
        """Clean up all active containers."""
        self.logger.info("Cleaning up active containers...")
        podman_utils.cleanup_all_containers()

    def run(self) -> None:
        """
        Execute evaluation on all instances using ThreadPoolExecutor.

        Uses tqdm progress bar to track execution progress.
        """
        if not self.instances:
            self.logger.warning("No instances to evaluate")
            return

        self.logger.info(f"Starting evaluation for agent: {self.agent_id}")
        self.logger.info(f"Evaluating {len(self.instances)} instances")
        self.logger.info(f"Using {self.config.nr_workers} parallel workers")

        results = {"success": 0, "failed": 0, "skipped": 0}
        interrupted = False

        # Manual executor management for proper shutdown control
        executor = ThreadPoolExecutor(max_workers=self.config.nr_workers)
        self.executor = executor

        try:
            # Submit all tasks
            future_to_instance = {
                executor.submit(evaluate_single_instance, inst, self.agent_id, self.config): inst
                for inst in self.instances
            }

            # Process completed tasks with progress bar
            with tqdm(total=len(self.instances), desc="Evaluation Progress", unit="instance") as pbar:
                for future in as_completed(future_to_instance):
                    instance = future_to_instance[future]

                    try:
                        success = future.result()
                        if success:
                            results["success"] += 1
                            status = "✅"
                        else:
                            results["failed"] += 1
                            status = "❌"

                        self.logger.info(f"{status} [{instance.id}] completed")

                    except Exception as e:
                        results["failed"] += 1
                        self.logger.error(f"❌ [{instance.id}] exception: {e}")

                    pbar.update(1)

        finally:
            if self.executor:
                self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = None
            self._cleanup_containers()

            # Print summary
            total = results["success"] + results["failed"]
            self.logger.info("\n" + "=" * 50)
            self.logger.info("Evaluation Summary:")
            self.logger.info(f"  Agent ID: {self.agent_id}")
            self.logger.info(f"  Total: {total}")
            self.logger.info(f"  Success: {results['success']}")
            self.logger.info(f"  Failed: {results['failed']}")
            self.logger.info("=" * 50)
