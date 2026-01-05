"""Data models for evaluation configuration and results."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, computed_field

from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata


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
            self.failed != -1  # Didn't crash
            and self.total >= 10  # Minimum test suite size
            and self.total < 10000  # Sanity check
        )


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
        followed = self.positive_rules_matched + (self.total_negative_rules - self.negative_rules_matched)
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


class EvaluationConfig(BaseModel):
    """Runtime configuration for evaluation execution."""

    instances_csv: Path
    agent_id: str
    output_dir: Path = Path("./output")
    nr_workers: int = Field(gt=0, default=4)
    timeout_test: int = Field(gt=0, default=600)  # 10 minutes
    timeout_rule: int = Field(gt=0, default=1200)  # 20 minutes
    force: bool = False

    class Config:
        arbitrary_types_allowed = True


class EvaluationResult(BaseModel):
    """Complete evaluation result for a single instance and agent."""

    instance_metadata: ExecutionInstanceMetadata
    agent_test_metrics: Optional[TestMetrics] = None
    agent_rule_metrics: RuleMetrics  # Required, not optional
    evaluation_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    class Config:
        arbitrary_types_allowed = True
