"""Validation logic for evaluation results."""

from enum import Enum

from refactoring_benchmark.analyze.baseline import load_baseline_bounds
from refactoring_benchmark.analyze.models import format_type_mode_label
from refactoring_benchmark.evaluation.models import EvaluationResult


class ValidityStatus(str, Enum):
    """Test validity status for an evaluation result."""

    VALID = "valid"
    NO_EXEC_ENV = "no_exec_env"
    INVALID_TESTS = "invalid_tests"
    NO_TEST_RESULTS = "no_test_results"
    NO_BASELINE = "no_baseline"


def check_test_validity(result: EvaluationResult, alpha: float = 0.1) -> ValidityStatus:
    """
    Check if agent test results are valid.

    Returns:
        ValidityStatus indicating the test validity:
        - VALID: Tests are valid and within expected range
        - NO_EXEC_ENV: No execution environment available (tests not applicable)
        - INVALID_TESTS: Test results are outside the expected baseline range
        - NO_BASELINE: No baseline test results available for the instance
    """
    if not 0 <= alpha <= 1:
        raise ValueError(f"alpha must be in [0, 1], got {alpha}")

    # If no execution environment, we don't care about test results
    if not result.instance_metadata.has_execution_environment:
        return ValidityStatus.NO_EXEC_ENV

    baseline_bounds = load_baseline_bounds(result.instance_metadata)
    if baseline_bounds is None:
        i = result.instance_metadata
        a = result.agent_config
        label = "unknown"
        if result.inference_metadata is not None:
            label = format_type_mode_label(
                result.inference_metadata.description_type,
                result.inference_metadata.mode,
                separator="/",
            )
        print(
            f"WARNING: No baseline test results found for {i.owner}/{i.repo}/{i.base_hash[:8]}. The agent's test are trivially valid. [{label}] (agent={a.id})."
        )
        return ValidityStatus.NO_BASELINE

    if result.agent_test_metrics is None:
        if result.inference_metadata.finish_reason != "success":
            i = result.instance_metadata
            a = result.agent_config
            desc = result.inference_metadata.description_type
            mode = result.inference_metadata.mode
            label = format_type_mode_label(desc, mode, separator="/")
            print(
                f"WARNING: `run_tests` for the agent {a.id} on instance {i.owner}/{i.repo}/{i.base_hash[:8]} [{label}] did not produce test results. However the agent also didn't finish successfully. finish_reason={result.inference_metadata.finish_reason}"
            )
        return ValidityStatus.NO_TEST_RESULTS

    agent_passed = result.agent_test_metrics.passed
    agent_failed = result.agent_test_metrics.failed

    # TODO: Consider flagging high-variance baseline suites to avoid overly wide or narrow bounds.
    if agent_passed >= baseline_bounds.min_passed and agent_failed <= baseline_bounds.max_failed:
        return ValidityStatus.VALID
    return ValidityStatus.INVALID_TESTS
