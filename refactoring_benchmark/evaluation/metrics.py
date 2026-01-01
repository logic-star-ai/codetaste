"""Core evaluation metrics and data models."""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, computed_field


class SetupQuality(str, Enum):
    """Quality of the test suite setup."""
    BOTH_VALID = "both_valid"
    ONLY_BASE_VALID = "only_base_valid"
    ONLY_GOLDEN_VALID = "only_golden_valid"
    NEITHER_VALID = "neither_valid"

    def is_sufficient(self) -> bool:
        """Whether we can meaningfully evaluate test success."""
        return self == SetupQuality.BOTH_VALID

    def can_evaluate_tests(self) -> bool:
        """Whether we have any valid test baseline."""
        return self in {
            SetupQuality.BOTH_VALID,
            SetupQuality.ONLY_BASE_VALID,
            SetupQuality.ONLY_GOLDEN_VALID
        }


class TestOutcome(str, Enum):
    """Outcome of test evaluation."""
    TEST_SUCCESS = "test_success"       # Both commits valid, agent tests in bounds
    TEST_FAIL = "test_fail"            # Both commits valid, agent tests out of bounds
    TEST_TRIVIAL = "test_trivial"      # Only one commit valid, can't properly evaluate
    TEST_NOT_SETUP = "test_not_setup"  # Neither commit valid, no test baseline
    TEST_ERROR = "test_error"          # Agent tests crashed/didn't run

    def is_meaningful(self) -> bool:
        """Whether this is a meaningful test result."""
        return self in {TestOutcome.TEST_SUCCESS, TestOutcome.TEST_FAIL}

    def is_problematic(self) -> bool:
        """Whether this indicates setup problems."""
        return self in {TestOutcome.TEST_TRIVIAL, TestOutcome.TEST_NOT_SETUP}


class TestMetrics(BaseModel):
    """Test execution metrics."""
    passed: int
    failed: int
    skipped: int = 0
    total: int
    error: Optional[str] = None

    @computed_field
    @property
    def pass_rate(self) -> float:
        """Fraction of tests that passed."""
        return self.passed / self.total if self.total > 0 else 0.0

    @computed_field
    @property
    def is_valid(self) -> bool:
        """Tests ran without crashing and have reasonable coverage."""
        return (
            self.failed != -1 and  # Didn't crash
            self.total >= 10 and   # Minimum test suite size
            self.total < 10000     # Sanity check
        )

    @computed_field
    @property
    def is_minimal_valid(self) -> bool:
        """More lenient validity check - just didn't crash."""
        return self.failed != -1 and self.total > 0


class RuleMetrics(BaseModel):
    """Rule evaluation metrics from SARIF output."""
    positive_rules_matched: int  # Good patterns found
    negative_rules_matched: int  # Bad patterns found (violations)
    total_positive_rules: int
    total_negative_rules: int

    @computed_field
    @property
    def ifr(self) -> float:
        """Instruction Following Rate.

        IFR = (positive_matched + negative_avoided) / total_rules
        """
        total = self.total_positive_rules + self.total_negative_rules
        if total == 0:
            return 1.0

        # Count successes: positive rules matched + negative rules avoided
        followed = self.positive_rules_matched + (
            self.total_negative_rules - self.negative_rules_matched
        )
        return followed / total

    @computed_field
    @property
    def positive_ifr(self) -> float:
        """Instruction following rate for positive rules only."""
        if self.total_positive_rules == 0:
            return 1.0
        return self.positive_rules_matched / self.total_positive_rules

    @computed_field
    @property
    def negative_ifr(self) -> float:
        """Instruction following rate for negative rules only (avoiding bad patterns)."""
        if self.total_negative_rules == 0:
            return 1.0
        avoided = self.total_negative_rules - self.negative_rules_matched
        return avoided / self.total_negative_rules


class AgentMetadata(BaseModel):
    """Metadata about the agent that performed the refactoring.

    This should be written by the agent to /output/agent_metadata.json
    """
    # Required fields
    agent_name: str = Field(..., description="Name/identifier of the agent")
    agent_version: str = Field(..., description="Version of the agent")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the agent ran"
    )

    # Model information (if applicable)
    model_name: Optional[str] = Field(None, description="Underlying model name")
    model_provider: Optional[str] = Field(None, description="Model provider")

    # Configuration
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, gt=0, description="Maximum tokens for generation")
    prompt_template: Optional[str] = Field(None, description="Prompt template identifier")

    # Execution details
    execution_time_seconds: Optional[float] = Field(None, ge=0, description="Total execution time")
    total_input_tokens: Optional[int] = Field(None, ge=0, description="Total input tokens")
    total_output_tokens: Optional[int] = Field(None, ge=0, description="Total output tokens")
    total_cost_usd: Optional[float] = Field(None, ge=0, description="Total cost in USD")

    # Agent-specific metadata
    custom_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Agent-specific configuration"
    )

    # Developer/research info
    developer: Optional[str] = Field(None, description="Agent developer or research team")
    experiment_id: Optional[str] = Field(None, description="Experiment identifier")
    notes: Optional[str] = Field(None, description="Additional notes")


class InstanceEvaluation(BaseModel):
    """Complete evaluation for one instance."""
    instance_id: str

    # Test metrics
    base_tests: TestMetrics
    golden_tests: TestMetrics
    agent_tests: Optional[TestMetrics] = None

    # Rule metrics
    agent_rules: Optional[RuleMetrics] = None

    # Agent information
    agent_metadata: Optional[AgentMetadata] = None

    @computed_field
    @property
    def setup_quality(self) -> SetupQuality:
        """Classify the quality of the test suite setup."""
        base_valid = self.base_tests.is_valid
        golden_valid = self.golden_tests.is_valid

        if base_valid and golden_valid:
            return SetupQuality.BOTH_VALID
        elif base_valid and not golden_valid:
            return SetupQuality.ONLY_BASE_VALID
        elif not base_valid and golden_valid:
            return SetupQuality.ONLY_GOLDEN_VALID
        else:
            return SetupQuality.NEITHER_VALID

    @computed_field
    @property
    def test_outcome(self) -> TestOutcome:
        """Categorize the test evaluation outcome."""

        # No agent tests available
        if not self.agent_tests:
            if self.setup_quality == SetupQuality.NEITHER_VALID:
                return TestOutcome.TEST_NOT_SETUP
            else:
                return TestOutcome.TEST_ERROR

        # Agent tests crashed
        if not self.agent_tests.is_minimal_valid:
            return TestOutcome.TEST_ERROR

        # Setup issues - can't properly evaluate
        if self.setup_quality == SetupQuality.NEITHER_VALID:
            return TestOutcome.TEST_NOT_SETUP

        if self.setup_quality in {
            SetupQuality.ONLY_BASE_VALID,
            SetupQuality.ONLY_GOLDEN_VALID
        }:
            return TestOutcome.TEST_TRIVIAL

        # Both commits valid - can properly evaluate
        assert self.setup_quality == SetupQuality.BOTH_VALID

        min_passed = min(self.base_tests.passed, self.golden_tests.passed)
        max_passed = max(self.base_tests.passed, self.golden_tests.passed)

        if min_passed <= self.agent_tests.passed <= max_passed:
            return TestOutcome.TEST_SUCCESS
        else:
            return TestOutcome.TEST_FAIL

    @computed_field
    @property
    def overall_success(self) -> bool:
        """Overall success based on test outcome and IFR.

        Success criteria:
        - test_success: Tests pass AND IFR >= 0.8
        - test_trivial: IFR >= 0.95 (very high bar, mark with warning)
        - test_not_setup: IFR >= 0.95 (very high bar, mark with warning)
        - test_fail: False (tests failed)
        - test_error: False (agent crashed)
        """
        if not self.agent_rules:
            return False

        outcome = self.test_outcome
        ifr = self.agent_rules.ifr

        if outcome == TestOutcome.TEST_SUCCESS:
            return ifr >= 0.8
        elif outcome == TestOutcome.TEST_TRIVIAL:
            return ifr >= 0.95
        elif outcome == TestOutcome.TEST_NOT_SETUP:
            return ifr >= 0.95
        else:  # TEST_FAIL or TEST_ERROR
            return False

    @computed_field
    @property
    def success_quality(self) -> Optional[str]:
        """Quality indicator for successful instances.

        Returns:
            "clean": test_success with good IFR (fully validated)
            "questionable": test_trivial or test_not_setup (flag for review)
            None: not successful
        """
        if not self.overall_success:
            return None

        if self.test_outcome == TestOutcome.TEST_SUCCESS:
            return "clean"
        else:
            return "questionable"

    @computed_field
    @property
    def agent_introduced_regressions(self) -> Optional[bool]:
        """Agent broke tests (only meaningful if both commits valid)."""
        if self.setup_quality != SetupQuality.BOTH_VALID or not self.agent_tests:
            return None

        max_passed = max(self.base_tests.passed, self.golden_tests.passed)
        return self.agent_tests.passed < max_passed

    @computed_field
    @property
    def agent_improved_tests(self) -> Optional[bool]:
        """Agent improved tests beyond golden (only meaningful if both commits valid)."""
        if self.setup_quality != SetupQuality.BOTH_VALID or not self.agent_tests:
            return None

        return self.agent_tests.passed > self.golden_tests.passed
