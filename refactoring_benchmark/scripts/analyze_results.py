"""Analyze evaluation results across all instances using the evaluation framework."""

import csv
import json
import sys
from pathlib import Path
from typing import List, Optional
import pandas as pd
from scipy.stats import pearsonr

from refactoring_benchmark.evaluation.metrics import (
    InstanceEvaluation,
    TestMetrics,
    RuleMetrics,
    AgentMetadata,
)
from refactoring_benchmark.utils.models import InstanceRow
from refactoring_benchmark.utils.logger import setup_logging, get_logger

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
CSV_FILE = PROJECT_ROOT / "instances.csv"
LOG_DIR = PROJECT_ROOT / "logs"

# Initialize logging
setup_logging(str(LOG_DIR))
logger = get_logger("analyze")


def parse_sarif_to_metrics(
    sarif_pos_path: Path, sarif_neg_path: Path
) -> Optional[RuleMetrics]:
    """Parse SARIF files to extract rule metrics.

    Args:
        sarif_pos_path: Path to positive rules SARIF file
        sarif_neg_path: Path to negative rules SARIF file

    Returns:
        RuleMetrics if parsing successful, None otherwise
    """
    try:
        # Parse positive rules
        positive_matched = 0
        total_positive = 0

        if sarif_pos_path.exists():
            with open(sarif_pos_path) as f:
                sarif_pos = json.load(f)

            # Count how many positive patterns were found
            if "runs" in sarif_pos:
                for run in sarif_pos["runs"]:
                    if "results" in run:
                        positive_matched = len(run["results"])

            # Count total positive rules
            if "runs" in sarif_pos:
                for run in sarif_pos["runs"]:
                    if "tool" in run and "driver" in run["tool"]:
                        if "rules" in run["tool"]["driver"]:
                            total_positive = len(run["tool"]["driver"]["rules"])

        # Parse negative rules
        negative_matched = 0
        total_negative = 0

        if sarif_neg_path.exists():
            with open(sarif_neg_path) as f:
                sarif_neg = json.load(f)

            # Count how many negative patterns were found (violations)
            if "runs" in sarif_neg:
                for run in sarif_neg["runs"]:
                    if "results" in run:
                        negative_matched = len(run["results"])

            # Count total negative rules
            if "runs" in sarif_neg:
                for run in sarif_neg["runs"]:
                    if "tool" in run and "driver" in run["tool"]:
                        if "rules" in run["tool"]["driver"]:
                            total_negative = len(run["tool"]["driver"]["rules"])

        return RuleMetrics(
            positive_rules_matched=positive_matched,
            negative_rules_matched=negative_matched,
            total_positive_rules=total_positive,
            total_negative_rules=total_negative,
        )

    except Exception as e:
        logger.error(f"Failed to parse SARIF files: {e}")
        return None


def load_instance_evaluation(row: InstanceRow) -> InstanceEvaluation:
    """Load all metrics for an instance.

    Args:
        row: Instance row from CSV

    Returns:
        InstanceEvaluation with all available metrics
    """
    # Load metadata (base and golden)
    metadata_path = Path(row.instance_dir()) / "metadata.json"

    if not metadata_path.exists():
        logger.warning(f"Metadata not found for {row.id}: {metadata_path}")
        # Return with minimal data
        return InstanceEvaluation(
            instance_id=row.id,
            base_tests=TestMetrics(passed=0, failed=-1, total=0),
            golden_tests=TestMetrics(passed=0, failed=-1, total=0),
        )

    with open(metadata_path) as f:
        metadata = json.load(f)

    base_tests = TestMetrics(**metadata["base_metrics"])
    golden_tests = TestMetrics(**metadata["golden_metrics"])

    # Load agent outputs
    output_dir = Path(row.instance_dir("output"))

    # Load agent metadata from static config + optional runtime metrics
    agent_metadata = None

    # Try to load static agent config (should be in agent/ directory or copied to output/)
    agent_config_path = output_dir / "agent_config.json"
    if not agent_config_path.exists():
        # Fallback: check project agent directory
        agent_config_path = PROJECT_ROOT / "agent" / "agent_config.json"

    if agent_config_path.exists():
        try:
            with open(agent_config_path) as f:
                config = json.load(f)

            # Load optional runtime metrics
            runtime_path = output_dir / "run_metrics.json"
            if runtime_path.exists():
                with open(runtime_path) as f:
                    runtime = json.load(f)
                # Merge: runtime overrides config
                config.update(runtime)

            # Add auto-generated timestamp if not present
            if "timestamp" not in config:
                from datetime import datetime

                config["timestamp"] = datetime.utcnow().isoformat() + "Z"

            agent_metadata = AgentMetadata(**config)
        except Exception as e:
            logger.warning(f"Failed to load agent metadata for {row.id}: {e}")
    else:
        logger.warning(f"No agent_config.json found for {row.id}")

    # Load agent test results from test_results/test_results.json
    test_results_path = output_dir / "test_results" / "test_results.json"
    agent_tests = None
    if test_results_path.exists():
        try:
            with open(test_results_path) as f:
                agent_tests = TestMetrics(**json.load(f))
        except Exception as e:
            logger.warning(f"Failed to load test results for {row.id}: {e}")

    # Load agent rule results from SARIF files
    sarif_pos = output_dir / "rules_positive.sarif"
    sarif_neg = output_dir / "rules_negative.sarif"
    agent_rules = None
    if sarif_pos.exists() or sarif_neg.exists():
        agent_rules = parse_sarif_to_metrics(sarif_pos, sarif_neg)

    return InstanceEvaluation(
        instance_id=row.id,
        base_tests=base_tests,
        golden_tests=golden_tests,
        agent_tests=agent_tests,
        agent_rules=agent_rules,
        agent_metadata=agent_metadata,
    )


def analyze_all() -> pd.DataFrame:
    """Analyze all instances and return summary DataFrame.

    Returns:
        DataFrame with evaluation results for all instances
    """
    instances = []

    if not CSV_FILE.exists():
        logger.error(f"Instances file not found: {CSV_FILE}")
        sys.exit(1)

    with open(CSV_FILE) as f:
        for row_dict in csv.DictReader(f):
            instances.append(InstanceRow(**row_dict))

    logger.info(f"Loading evaluation for {len(instances)} instances...")

    evaluations = [load_instance_evaluation(row) for row in instances]

    # Convert to DataFrame
    records = []
    for ev in evaluations:
        record = {
            "instance_id": ev.instance_id,
            # Setup quality
            "setup_quality": ev.setup_quality.value,
            "test_outcome": ev.test_outcome.value,
            # Agent metadata
            "agent_name": ev.agent_metadata.agent_name if ev.agent_metadata else None,
            "agent_version": (
                ev.agent_metadata.agent_version if ev.agent_metadata else None
            ),
            "model_name": ev.agent_metadata.model_name if ev.agent_metadata else None,
            "model_provider": (
                ev.agent_metadata.model_provider if ev.agent_metadata else None
            ),
            "temperature": ev.agent_metadata.temperature if ev.agent_metadata else None,
            "execution_time": (
                ev.agent_metadata.execution_time_seconds if ev.agent_metadata else None
            ),
            "total_tokens": (
                (
                    (ev.agent_metadata.total_input_tokens or 0)
                    + (ev.agent_metadata.total_output_tokens or 0)
                )
                if ev.agent_metadata and ev.agent_metadata.total_input_tokens
                else None
            ),
            "cost_usd": ev.agent_metadata.total_cost_usd if ev.agent_metadata else None,
            "developer": ev.agent_metadata.developer if ev.agent_metadata else None,
            "experiment_id": (
                ev.agent_metadata.experiment_id if ev.agent_metadata else None
            ),
            # Test metrics
            "base_passed": ev.base_tests.passed,
            "base_total": ev.base_tests.total,
            "base_valid": ev.base_tests.is_valid,
            "golden_passed": ev.golden_tests.passed,
            "golden_total": ev.golden_tests.total,
            "golden_valid": ev.golden_tests.is_valid,
            "agent_passed": ev.agent_tests.passed if ev.agent_tests else None,
            "agent_total": ev.agent_tests.total if ev.agent_tests else None,
            "agent_valid": ev.agent_tests.is_valid if ev.agent_tests else None,
            # Derived (only meaningful for both_valid)
            "agent_regressed": ev.agent_introduced_regressions,
            "agent_improved": ev.agent_improved_tests,
            # Rule metrics
            "ifr": ev.agent_rules.ifr if ev.agent_rules else None,
            "positive_ifr": ev.agent_rules.positive_ifr if ev.agent_rules else None,
            "negative_ifr": ev.agent_rules.negative_ifr if ev.agent_rules else None,
            # Success
            "overall_success": ev.overall_success,
            "success_quality": ev.success_quality,
        }
        records.append(record)

    return pd.DataFrame(records)


def print_summary(df: pd.DataFrame):
    """Print evaluation summary with clear test outcome breakdown."""
    print("=" * 80)
    print("EVALUATION ANALYSIS")
    print("=" * 80)

    total = len(df)
    completed = df["agent_passed"].notna().sum()

    print(f"\nTotal Instances: {total}")
    print(f"Agent Completed: {completed}/{total} ({completed/total:.1%})")

    if completed == 0:
        logger.warning("No completed instances to analyze")
        return

    df_completed = df[df["agent_passed"].notna()]

    # Test outcome breakdown
    print(f"\n{'='*80}")
    print("TEST OUTCOMES")
    print(f"{'='*80}")

    outcome_counts = df_completed["test_outcome"].value_counts()
    outcome_labels = {
        "test_success": "✓ Test Success (properly evaluated)",
        "test_fail": "✗ Test Fail (properly evaluated)",
        "test_trivial": "⚠ Test Trivial (weak evaluation)",
        "test_not_setup": "⚠⚠ Test Not Setup (no baseline)",
        "test_error": "✗ Test Error (agent crashed)",
    }

    for outcome in [
        "test_success",
        "test_fail",
        "test_trivial",
        "test_not_setup",
        "test_error",
    ]:
        count = outcome_counts.get(outcome, 0)
        pct = count / completed * 100
        label = outcome_labels.get(outcome, outcome)
        print(f"{label:50s}: {count:4d} ({pct:5.1f}%)")

    # Key statistics
    meaningful = outcome_counts.get("test_success", 0) + outcome_counts.get(
        "test_fail", 0
    )
    problematic = outcome_counts.get("test_trivial", 0) + outcome_counts.get(
        "test_not_setup", 0
    )

    print(f"\nMeaningful test results: {meaningful} ({meaningful/completed:.1%})")
    print(f"Problematic setups:      {problematic} ({problematic/completed:.1%})")

    # Success breakdown
    print(f"\n{'='*80}")
    print("SUCCESS BREAKDOWN")
    print(f"{'='*80}")

    total_success = df_completed["overall_success"].sum()
    success_rate = df_completed["overall_success"].mean()

    print(f"\nTotal Success: {total_success}/{completed} ({success_rate:.1%})")

    # Success by test outcome
    df_success = df_completed[df_completed["overall_success"] == True]

    if len(df_success) > 0:
        print(f"\nSuccess by test outcome:")
        for outcome in ["test_success", "test_trivial", "test_not_setup"]:
            count = (df_success["test_outcome"] == outcome).sum()
            if count > 0:
                pct = count / total_success * 100
                flag = "" if outcome == "test_success" else " ⚠"
                print(f"  {outcome:20s}: {count:4d} ({pct:5.1f}%){flag}")

        # Clean vs questionable success
        clean = (df_success["success_quality"] == "clean").sum()
        questionable = (df_success["success_quality"] == "questionable").sum()

        print(f"\nSuccess quality:")
        print(
            f"  Clean (fully validated):        {clean:4d} ({clean/total_success:.1%})"
        )
        print(
            f"  Questionable (weak validation): {questionable:4d} ({questionable/total_success:.1%})"
        )

        if questionable > 0:
            print(
                f"\n  ⚠ WARNING: {questionable} successes have questionable validation"
            )
            print(f"    due to incomplete test setup. Review carefully.")

    # Analysis by test outcome
    print(f"\n{'='*80}")
    print("ANALYSIS BY TEST OUTCOME")
    print(f"{'='*80}")

    for outcome in ["test_success", "test_fail", "test_trivial", "test_not_setup"]:
        df_outcome = df_completed[df_completed["test_outcome"] == outcome]

        if len(df_outcome) == 0:
            continue

        n = len(df_outcome)
        success_rate_outcome = (
            df_outcome["overall_success"].mean() if len(df_outcome) > 0 else 0
        )
        avg_ifr = df_outcome["ifr"].mean()

        print(f"\n{outcome.replace('_', ' ').title()}:")
        print(f"  N = {n}")
        print(f"  Success Rate: {success_rate_outcome:.1%}")
        print(f"  Avg IFR: {avg_ifr:.1%}")

        # IFR threshold used
        if outcome == "test_success":
            print(f"  IFR threshold: >= 0.80")
        elif outcome in ["test_trivial", "test_not_setup"]:
            print(f"  IFR threshold: >= 0.95 (higher bar)")

        # Additional metrics for meaningful outcomes
        if outcome == "test_success":
            regressed = df_outcome["agent_regressed"].sum()
            improved = df_outcome["agent_improved"].sum()
            print(f"  Regressions: {regressed} ({regressed/n:.1%})")
            print(f"  Improvements: {improved} ({improved/n:.1%})")

        elif outcome == "test_fail":
            regressed = df_outcome["agent_regressed"].sum()
            print(f"  Regressions: {regressed} ({regressed/n:.1%})")

    # Conditional analysis (only for test_success)
    df_test_success = df_completed[df_completed["test_outcome"] == "test_success"]

    if len(df_test_success) > 10:
        print(f"\n{'='*80}")
        print("CONDITIONAL ANALYSIS (test_success only)")
        print(f"{'='*80}")

        df_with_ifr = df_test_success[df_test_success["ifr"].notna()]

        if len(df_with_ifr) > 5:
            success = df_with_ifr["overall_success"]

            print(
                f"\nE[IFR | overall_success]: {df_with_ifr[success]['ifr'].mean():.1%}"
            )
            print(
                f"E[IFR | overall_failure]: {df_with_ifr[~success]['ifr'].mean():.1%}"
            )
            print(f"Pr[overall_success]: {success.mean():.1%}")

            high_ifr = df_with_ifr["ifr"] >= 0.8
            print(
                f"Pr[overall_success | IFR >= 0.8]: {df_with_ifr[high_ifr]['overall_success'].mean():.1%}"
            )

            # Correlation
            if len(df_with_ifr) > 5:
                try:
                    ifr_values = df_with_ifr["ifr"].values
                    success_values = df_with_ifr["overall_success"].astype(float).values
                    corr, p_val = pearsonr(ifr_values, success_values)
                    print(
                        f"\nCorrelation(IFR, overall_success): r={corr:.3f}, p={p_val:.4f}"
                    )
                except ImportError:
                    logger.warning("scipy not available for correlation analysis")


def main():
    """Main entry point for analysis script."""
    logger.info("Starting results analysis...")

    # Load all evaluations
    df = analyze_all()

    # Save to CSV
    output_file = PROJECT_ROOT / "analysis_results.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"Saved results to {output_file}")

    # Print summary
    print_summary(df)

    logger.info("Analysis complete")


if __name__ == "__main__":
    main()
