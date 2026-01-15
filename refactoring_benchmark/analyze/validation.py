"""Validation logic for evaluation results."""

from enum import Enum

from refactoring_benchmark.evaluation.models import EvaluationResult


class ValidityStatus(str, Enum):
    """Test validity status for an evaluation result."""

    VALID = "valid"
    NO_EXEC_ENV = "no_exec_env"
    INVALID_TESTS = "invalid_tests"
    NO_TEST_RESULTS = "no_test_results"


def check_test_validity(result: EvaluationResult) -> ValidityStatus:
    """
    Check if agent test results are valid.

    Returns:
        ValidityStatus indicating the test validity:
        - VALID: Tests are valid and within expected range
        - NO_EXEC_ENV: No execution environment available (tests not applicable)
        - INVALID_TESTS: Test results are outside the expected base/golden range
    """
    # If no execution environment, we don't care about test results
    if not result.instance_metadata.has_execution_environment:
        return ValidityStatus.NO_EXEC_ENV
    
    if result.agent_test_metrics is None:
        if result.inference_metadata.finish_reason != "success":
            i = result.instance_metadata
            a = result.agent_config
            print(f"WARNING: `run_tests` for the agent {a.id} on instance {i.owner}/{i.repo}/{i.base_hash[:8]} did not produce test results. However the agent also didn't finish successfully. finish_reason={result.inference_metadata.finish_reason}")
        return ValidityStatus.NO_TEST_RESULTS

    agent_passed = result.agent_test_metrics.passed
    agent_failed = result.agent_test_metrics.failed
    base_passed = result.instance_metadata.base_metrics.passed
    base_failed = result.instance_metadata.base_metrics.failed
    golden_passed = result.instance_metadata.golden_metrics.passed
    golden_failed = result.instance_metadata.golden_metrics.failed
    min_passed = min(base_passed, golden_passed)
    max_passed = max(base_passed, golden_passed)
    max_failed = max(base_failed, golden_failed)
    min_failed = min(base_failed, golden_failed)


    if min_failed == -1: # No valid test results in either base or golden, accept any results
        return ValidityStatus.VALID
    elif result.agent_test_metrics is None:
        return ValidityStatus.NO_TEST_RESULTS
    elif 0.9 * min_passed <= agent_passed <= 1.1 * max_passed and agent_failed <= max_failed:
        return ValidityStatus.VALID
    else:
        return ValidityStatus.INVALID_TESTS
