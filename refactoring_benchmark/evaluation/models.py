"""Data models for evaluation configuration and results."""

from datetime import datetime
from pathlib import Path
from typing import Optional, Type, TypeVar

from pydantic import BaseModel, Field, computed_field

from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata
from refactoring_benchmark.inference.models import AgentConfig, InferenceMetadata

T = TypeVar("T", bound="EvaluationResult")


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
    timeout_test: int = Field(gt=0, default=1200)  # 20 minutes
    timeout_rule: int = Field(gt=0, default=1200)  # 20 minutes
    force: bool = False
    retry_null_tests: bool = False

    class Config:
        arbitrary_types_allowed = True


class EvaluationResult(BaseModel):
    """Complete evaluation result for a single instance and agent."""

    instance_metadata: ExecutionInstanceMetadata
    agent_config: AgentConfig
    agent_test_metrics: Optional[TestMetrics] = None
    agent_rule_metrics: RuleMetrics
    inference_metadata: Optional[InferenceMetadata] = None
    evaluation_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    eval_dir: Optional[Path] = Field(default=None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def save_to_json(self, file_path: str | Path):
        """Save evaluation result to a JSON file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4))

    @classmethod
    def load_from_json(cls: Type[T], file_path: str | Path) -> T:
        """Load evaluation result from a JSON file.

        Also attempts to load inference_metadata.json from the parent directory if it exists.
        The expected structure is:
            {output_dir}/{owner}/{repo}/{hash}/{agent_id}/inference_metadata.json
            {output_dir}/{owner}/{repo}/{hash}/{agent_id}/evaluation/evaluation_result.json
        """
        path = Path(file_path)
        with path.open("r", encoding="utf-8") as f:
            result = cls.model_validate_json(f.read())

        # Path structure: {output_dir}/{owner}/{repo}/{hash}/{agent_id}/evaluation/evaluation_result.json
        result.eval_dir = path.parent

        # If no embedded metadata, try to load from standalone file
        if result.inference_metadata is None:
            inference_metadata_path = path.parent.parent / "inference_metadata.json"
            if inference_metadata_path.exists():
                try:
                    with inference_metadata_path.open("r", encoding="utf-8") as f:
                        result.inference_metadata = InferenceMetadata.model_validate_json(f.read())
                except Exception:
                    pass

        return result
