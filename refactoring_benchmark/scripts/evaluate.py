"""Evaluate benchmark instances using test and rule-based metrics."""

import csv
import json
import os
import subprocess
import sys
from typing import Optional, Dict, Any, Tuple

import yaml

from refactoring_benchmark.utils.logger import get_logger, setup_logging
from refactoring_benchmark.utils.models import InstanceRow, Metrics

# Constants
CSV_FILE = "instances.csv"
LOG_DIR = "logs"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Initialize Logging
setup_logging(LOG_DIR)
eval_logger = get_logger("evaluate")


class EvaluationResult:
    """Stores evaluation results for a single instance."""

    def __init__(self, instance_id: str):
        self.instance_id = instance_id
        self.test_metrics: Optional[Metrics] = None
        self.rule_results_positive: Optional[float] = None
        self.rule_results_negative: Optional[float] = None
        self.rule_results_total: Optional[float] = None
        self.test_success: bool = False
        self.error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "instance_id": self.instance_id,
            "test_success": self.test_success,
        }

        if self.test_metrics:
            result["test_metrics"] = {
                "passed": self.test_metrics.passed,
                "failed": self.test_metrics.failed,
                "skipped": self.test_metrics.skipped,
                "total": self.test_metrics.total,
            }

        if self.rule_results_positive is not None:
            result["rule_results_positive"] = self.rule_results_positive

        if self.rule_results_negative is not None:
            result["rule_results_negative"] = self.rule_results_negative

        if self.rule_results_total is not None:
            result["rule_results_total"] = self.rule_results_total

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

    test_output_dir = os.path.join(instance_output_dir, "test_results")
    os.makedirs(test_output_dir, exist_ok=True)

    try:
        run_cmds = [
            "podman",
            "run",
            "--rm",
            "-v",
            f"{prediction_diff}:/input/patch.diff",
            "-v",
            f"{test_output_dir}:/output",
            f"{instance_row.runtime_image}",
            "eval_test",
        ]

        eval_logger.info(f"[{instance_row.id}]: Running: {' '.join(run_cmds)}")

        result = subprocess.run(run_cmds, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=600)

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
        eval_logger.debug(f"[{instance_row.id}]: Full output:\n{result.stdout}")
        eval_logger.debug(f"[{instance_row.id}]: Error output:\n{result.stderr}")
        return None

    except subprocess.TimeoutExpired:
        eval_logger.error(f"[{instance_row.id}]: Test evaluation timed out")
        return None
    except Exception as e:
        eval_logger.error(f"[{instance_row.id}]: Test evaluation failed: {e}")
        return None


def parse_sarif_results(sarif_path: str, rules_path: str) -> Dict[str, Tuple[int, int, int]]:
    """
    Parse results into a dictionary: RULE_ID -> (base_count, agent_count, golden_count).
    """
    results = {}

    if not os.path.exists(rules_path):
        eval_logger.warning(f"Rules file not found: {rules_path}")
        return results

    try:
        with open(rules_path, "r") as f:
            rules_data = yaml.safe_load(f)

        rules_metadata = {}
        if "rules" in rules_data:
            for rule in rules_data["rules"]:
                rule_id = rule.get("id")
                if rule_id and "metadata" in rule:
                    metadata = rule["metadata"]
                    base_count = metadata.get("nr_legacy_patterns", 0)
                    golden_count = metadata.get("nr_refactored_patterns", 0)
                    rules_metadata[rule_id] = (base_count, golden_count)
    except Exception as e:
        eval_logger.error(f"Failed to parse rules file {rules_path}: {e}")
        return results

    agent_counts = {}
    if os.path.exists(sarif_path):
        try:
            with open(sarif_path, "r") as f:
                sarif_data = json.load(f)

            if "runs" in sarif_data:
                for run in sarif_data["runs"]:
                    if "results" in run:
                        for result in run["results"]:
                            rule_id = result.get("ruleId")
                            if rule_id:
                                clean_id = rule_id.split(".")[-1]
                                agent_counts[clean_id] = agent_counts.get(clean_id, 0) + 1
        except Exception as e:
            eval_logger.error(f"Failed to parse SARIF file {sarif_path}: {e}")
    else:
        eval_logger.warning(f"SARIF file not found: {sarif_path}")

    for rule_id, (base_count, golden_count) in rules_metadata.items():
        agent_count = agent_counts.get(rule_id, 0)
        results[rule_id] = (base_count, agent_count, golden_count)

    return results


def run_rule_evaluation(
    instance_row: InstanceRow,
) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """
    Run rule-based evaluation. Returns (positive_rate, negative_rate, total_rate).
    """
    instance_output_dir = os.path.join(PROJECT_ROOT, instance_row.instance_dir("output"))
    prediction_diff = os.path.join(instance_output_dir, "prediction.diff")

    if not os.path.exists(prediction_diff):
        eval_logger.warning(f"[{instance_row.id}]: No prediction.diff found at {prediction_diff}")
        return None, None, None

    eval_logger.info(f"[{instance_row.id}]: Running rule evaluation...")

    try:
        run_cmds = [
            "podman",
            "run",
            "--rm",
            "-v",
            f"{prediction_diff}:/input/patch.diff",
            "-v",
            f"{instance_output_dir}:/output",
            f"{instance_row.runtime_image}",
            "eval_rule",
        ]

        subprocess.run(run_cmds, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=1200)

        sarif_pos = os.path.join(instance_output_dir, "rules_positive.sarif")
        sarif_neg = os.path.join(instance_output_dir, "rules_negative.sarif")
        rules_pos = os.path.join(instance_output_dir, "rules_positive.yml")
        rules_neg = os.path.join(instance_output_dir, "rules_negative.yml")

        pos_results = parse_sarif_results(sarif_pos, rules_pos)
        pos_satisfied = sum(1 for b, a, g in pos_results.values() if a > 0)
        pos_total = len(pos_results)

        neg_results = parse_sarif_results(sarif_neg, rules_neg)
        neg_satisfied = sum(1 for b, a, g in neg_results.values() if a == 0)
        neg_total = len(neg_results)

        share_pos = pos_satisfied / pos_total if pos_total > 0 else None
        share_neg = neg_satisfied / neg_total if neg_total > 0 else None

        total_satisfied = pos_satisfied + neg_satisfied
        total_rules = pos_total + neg_total
        share_total = total_satisfied / total_rules if total_rules > 0 else None

        return share_pos, share_neg, share_total

    except subprocess.TimeoutExpired:
        eval_logger.error(f"[{instance_row.id}]: Rule evaluation timed out")
        return None, None, None
    except Exception as e:
        eval_logger.error(f"[{instance_row.id}]: Rule evaluation failed: {e}")
        return None, None, None


def evaluate_instance(instance_row: InstanceRow) -> EvaluationResult:
    """Evaluate a single benchmark instance."""
    result = EvaluationResult(instance_row.id)
    eval_logger.info(f"\n{'='*60}\nEvaluating: {instance_row.display_path}\n{'='*60}")

    instance_output_dir = os.path.join(PROJECT_ROOT, instance_row.instance_dir("output"))
    prediction_diff = os.path.join(instance_output_dir, "prediction.diff")

    if not os.path.exists(prediction_diff):
        result.error = f"No prediction.diff found at {prediction_diff}"
        eval_logger.error(f"[{instance_row.id}]: {result.error}")
        return result

    test_metrics = run_test_evaluation(instance_row)
    result.test_metrics = test_metrics
    result.test_success = test_metrics is not None and test_metrics.failed == 0

    pos, neg, total = run_rule_evaluation(instance_row)
    result.rule_results_positive = pos
    result.rule_results_negative = neg
    result.rule_results_total = total

    eval_logger.info(
        f"[{instance_row.id}]: Instruction Following Rate: "
        f"{pos if pos is not None else 0:.2f} (pos), "
        f"{neg if neg is not None else 0:.2f} (neg), "
        f"{total if total is not None else 0:.2f} (total)"
    )

    return result


def main():
    """Main entry point."""
    eval_logger.info("Starting evaluation process...")

    instances = []
    if not os.path.exists(CSV_FILE):
        eval_logger.error(f"{CSV_FILE} not found.")
        sys.exit(1)

    with open(CSV_FILE, "r") as f:
        for row in csv.DictReader(f):
            instances.append(InstanceRow(**row))

    if not instances:
        eval_logger.error("No instances found in instances.csv")
        sys.exit(1)

    instances = instances[:15]

    eval_logger.info(f"Found {len(instances)} instances to evaluate")

    results: list[EvaluationResult] = []
    for instance in instances:
        results.append(evaluate_instance(instance))

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
            indent=2,
        )

    eval_logger.info(f"\n{'='*60}\nEvaluation complete!\nResults: {results_file}")

    rule_successes = sum(r.rule_results_total for r in results if r.rule_results_total is not None)
    errors = sum(1 for r in results if r.error)

    eval_logger.info(
        f"Summary:\n Total: {len(instances)}\n Rule Fraction: {rule_successes:.2f}/{len(instances)}\n Errors: {errors}\n{'='*60}"
    )


if __name__ == "__main__":
    main()
