"""Evaluate benchmark instances using test and rule-based metrics."""
import csv
import json
import os
import subprocess
import sys
from typing import Optional, Dict, Any

from refactoring_benchmark.utils.logger import get_logger, setup_logging
from refactoring_benchmark.utils.models import InstanceRow, Metrics


CSV_FILE = "instances.csv"
LOG_DIR = "logs"
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")

setup_logging(LOG_DIR)
eval_logger = get_logger("evaluate")


class EvaluationResult:
    """Stores evaluation results for a single instance."""

    def __init__(self, instance_id: str):
        self.instance_id = instance_id
        self.test_metrics: Optional[Metrics] = None
        self.rule_results_positive: Optional[Dict[str, Any]] = None
        self.rule_results_negative: Optional[Dict[str, Any]] = None
        self.test_success: bool = False
        self.rule_success: bool = False
        self.error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "instance_id": self.instance_id,
            "test_success": self.test_success,
            "rule_success": self.rule_success,
        }

        if self.test_metrics:
            result["test_metrics"] = {
                "passed": self.test_metrics.passed,
                "failed": self.test_metrics.failed,
                "skipped": self.test_metrics.skipped,
                "total": self.test_metrics.total,
            }

        if self.rule_results_positive:
            result["rule_results_positive"] = self.rule_results_positive

        if self.rule_results_negative:
            result["rule_results_negative"] = self.rule_results_negative

        if self.error:
            result["error"] = self.error

        return result


def run_test_evaluation(instance_row: InstanceRow) -> Optional[Metrics]:
    """
    Run test evaluation on a benchmark instance.

    Args:
        instance_row: The benchmark instance row to evaluate

    Returns:
        Test metrics if successful, None otherwise
    """
    instance_output_dir = os.path.join(PROJECT_ROOT, instance_row.instance_dir("output"))
    prediction_diff = os.path.join(instance_output_dir, "prediction.diff")

    if not os.path.exists(prediction_diff):
        eval_logger.warning(f"[{instance_row.id}]: No prediction.diff found at {prediction_diff}")
        return None

    eval_logger.info(f"[{instance_row.id}]: Running test evaluation...")

    # Create a temporary output directory for test results
    test_output_dir = os.path.join(instance_output_dir, "test_results")
    os.makedirs(test_output_dir, exist_ok=True)

    try:
        run_cmds = [
            "podman", "run", "--rm",
            "-v", f"{prediction_diff}:/input/patch.diff",
            "-v", f"{test_output_dir}:/output",
            f"{instance_row.runtime_image}",
            "eval_test"
        ]

        eval_logger.info(f"[{instance_row.id}]: Running: {' '.join(run_cmds)}")

        result = subprocess.run(
            run_cmds,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        # Parse test metrics from output
        # The run_tests script outputs JSON as the last line
        output_lines = result.stdout.strip().split("\n")

        for line in reversed(output_lines):
            try:
                data = json.loads(line)
                metrics = Metrics(**data)
                eval_logger.info(f"[{instance_row.id}]: Test metrics: {metrics.model_dump()}")
                return metrics
            except (json.JSONDecodeError, ValueError):
                continue

        eval_logger.warning(f"[{instance_row.id}]: Could not parse test metrics from output")
        return None

    except subprocess.TimeoutExpired:
        eval_logger.error(f"[{instance_row.id}]: Test evaluation timed out")
        return None
    except Exception as e:
        eval_logger.error(f"[{instance_row.id}]: Test evaluation failed: {e}")
        return None


def parse_sarif_results(sarif_path: str) -> Optional[Dict[str, Any]]:
    """
    Parse SARIF file and extract key metrics.

    Args:
        sarif_path: Path to SARIF file

    Returns:
        Dictionary with findings count and path
    """
    if not os.path.exists(sarif_path):
        return None

    try:
        with open(sarif_path, 'r') as f:
            sarif_data = json.load(f)

        # Extract key metrics from SARIF
        total_results = 0
        if "runs" in sarif_data:
            for run in sarif_data["runs"]:
                if "results" in run:
                    total_results += len(run["results"])

        return {
            "total_findings": total_results,
            "sarif_path": sarif_path,
        }
    except Exception as e:
        eval_logger.error(f"Failed to parse SARIF at {sarif_path}: {e}")
        return None


def run_rule_evaluation(instance_row: InstanceRow) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Run rule-based (static analysis) evaluation on a benchmark instance.
    Runs separate scans for positive and negative rules.

    Args:
        instance_row: The benchmark instance row to evaluate

    Returns:
        Tuple of (positive_results, negative_results)
    """
    instance_output_dir = os.path.join(PROJECT_ROOT, instance_row.instance_dir("output"))
    prediction_diff = os.path.join(instance_output_dir, "prediction.diff")

    if not os.path.exists(prediction_diff):
        eval_logger.warning(f"[{instance_row.id}]: No prediction.diff found at {prediction_diff}")
        return None, None

    eval_logger.info(f"[{instance_row.id}]: Running rule evaluation...")

    sarif_output_positive = os.path.join(instance_output_dir, "rules_positive.sarif")
    sarif_output_negative = os.path.join(instance_output_dir, "rules_negative.sarif")

    try:
        run_cmds = [
            "podman", "run", "--rm",
            "-v", f"{prediction_diff}:/input/patch.diff",
            "-v", f"{instance_output_dir}:/output",
            f"{instance_row.runtime_image}",
            "eval_rule"
        ]

        eval_logger.info(f"[{instance_row.id}]: Running: {' '.join(run_cmds)}")

        subprocess.run(
            run_cmds,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        # Parse both SARIF outputs
        positive_results = parse_sarif_results(sarif_output_positive)
        negative_results = parse_sarif_results(sarif_output_negative)

        if positive_results:
            eval_logger.info(f"[{instance_row.id}]: Positive rule findings: {positive_results['total_findings']}")
        else:
            eval_logger.warning(f"[{instance_row.id}]: No positive SARIF output found")

        if negative_results:
            eval_logger.info(f"[{instance_row.id}]: Negative rule findings: {negative_results['total_findings']}")
        else:
            eval_logger.warning(f"[{instance_row.id}]: No negative SARIF output found")

        return positive_results, negative_results

    except subprocess.TimeoutExpired:
        eval_logger.error(f"[{instance_row.id}]: Rule evaluation timed out")
        return None, None
    except Exception as e:
        eval_logger.error(f"[{instance_row.id}]: Rule evaluation failed: {e}")
        return None, None


def evaluate_instance(instance_row: InstanceRow) -> EvaluationResult:
    """
    Evaluate a single benchmark instance.

    Args:
        instance_row: The benchmark instance row to evaluate

    Returns:
        EvaluationResult containing all metrics and status
    """
    result = EvaluationResult(instance_row.id)

    eval_logger.info(f"\n{'='*60}")
    eval_logger.info(f"Evaluating: {instance_row.display_path}")
    eval_logger.info(f"{'='*60}")

    # Check if prediction.diff exists
    instance_output_dir = os.path.join(PROJECT_ROOT, instance_row.instance_dir("output"))
    prediction_diff = os.path.join(instance_output_dir, "prediction.diff")

    if not os.path.exists(prediction_diff):
        result.error = f"No prediction.diff found at {prediction_diff}"
        eval_logger.error(f"[{instance_row.id}]: {result.error}")
        return result


    # Run rule evaluation (both positive and negative)
    positive_results, negative_results = run_rule_evaluation(instance_row)
    if positive_results:
        result.rule_results_positive = positive_results
    if negative_results:
        result.rule_results_negative = negative_results

    # Consider rule successful if at least one evaluation completed
    result.rule_success = positive_results is not None or negative_results is not None

    # # Run test evaluation
    # # TODO: THE FILE IS CURRENTLY JUST BOILERPLATE TO SEE IF ENTRYPOINT WORKS CORRECTLY
    # test_metrics = run_test_evaluation(instance_row)
    # if test_metrics:
    #     result.test_metrics = test_metrics
    #     # Consider test successful if no failures and at least some tests passed
    #     result.test_success = test_metrics.failed == 0 and test_metrics.passed > 0

    # Log summary
    eval_logger.info(f"\n[{instance_row.id}] Summary:")
    eval_logger.info(f"  Test Success: {result.test_success}")
    if result.test_metrics:
        eval_logger.info(f"  Test Metrics: {result.test_metrics.model_dump()}")
    eval_logger.info(f"  Rule Success: {result.rule_success}")
    if result.rule_results_positive:
        eval_logger.info(f"  Positive Rule Findings: {result.rule_results_positive.get('total_findings', 0)}")
    if result.rule_results_negative:
        eval_logger.info(f"  Negative Rule Findings: {result.rule_results_negative.get('total_findings', 0)}")

    return result


def main():
    """Main entry point for the evaluation script."""
    eval_logger.info("Starting evaluation process...")

    # Read instances from CSV
    instances = []
    with open(CSV_FILE, "r") as f:
        for row in csv.DictReader(f):
            instances.append(InstanceRow(**row))

    if not instances:
        eval_logger.error("No instances found in instances.csv")
        sys.exit(1)

    eval_logger.info(f"Found {len(instances)} instances to evaluate")

    # Evaluate each instance
    results = []
    for instance in instances[:2]:
        result = evaluate_instance(instance)
        results.append(result)

    # Save aggregated results
    output_dir = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(output_dir, exist_ok=True)

    results_file = os.path.join(output_dir, "evaluation_results.json")
    with open(results_file, "w") as f:
        json.dump(
            {
                "total_instances": len(instances),
                "results": [r.to_dict() for r in results],
            },
            f,
            indent=2
        )

    eval_logger.info(f"\n{'='*60}")
    eval_logger.info(f"Evaluation complete!")
    eval_logger.info(f"Results saved to: {results_file}")

    # Print summary statistics
    test_successes = sum(1 for r in results if r.test_success)
    rule_successes = sum(1 for r in results if r.rule_success)
    errors = sum(1 for r in results if r.error)

    eval_logger.info(f"\nSummary:")
    eval_logger.info(f"  Total Instances: {len(instances)}")
    eval_logger.info(f"  Test Successes: {test_successes}/{len(instances)}")
    eval_logger.info(f"  Rule Successes: {rule_successes}/{len(instances)}")
    eval_logger.info(f"  Errors: {errors}/{len(instances)}")
    eval_logger.info(f"{'='*60}")


if __name__ == "__main__":
    main()
