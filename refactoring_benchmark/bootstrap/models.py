"""Data models for bootstrap configuration."""

from pathlib import Path
from typing import Optional, Type, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T", bound="ExecutionInstanceMetadata")


class BootstrapConfig(BaseModel):
    """Runtime configuration for bootstrap execution."""

    instances_csv: Path
    nr_workers: int = Field(gt=0, default=4)
    force_runtime_build: bool = False
    rerun_metrics: bool = False
    force_full_build: bool = False
    api_key: str
    base_image: str = "benchmark/benchmark-base-all"
    timeout_bootstrap: int = Field(gt=0, default=7200)  # 2 hours
    supported_languages: list[str] = Field(default_factory=lambda: ["python", "javascript", "java", "c", "go", "rust"])

    class Config:
        arbitrary_types_allowed = True


class Metrics(BaseModel):
    """Test execution metrics."""

    passed: int = 0
    failed: int = 0
    skipped: int = 0
    total: int = 0
    error: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        """At least 10 tests, at least 30% passed."""
        if self.total == 0:
            return False
        return self.error is None and self.total >= 10 and (self.passed / self.total) >= 0.3


class ExecutionInstanceMetadata(BaseModel):
    """Metadata for an execution instance."""

    owner: str
    repo: str
    base_hash: str
    golden_hash: str
    golden_metrics: Optional[Metrics] = None
    base_metrics: Optional[Metrics] = None
    setup_image: Optional[str] = None
    runtime_image: Optional[str] = None
    has_execution_environment: Optional[bool] = None
    reason_no_execution_environment: str = ""

    def save_to_json(self, file_path: str | Path):
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4))

    @classmethod
    def load_from_json(cls: Type[T], file_path: str | Path) -> T:
        path = Path(file_path)
        with path.open("r", encoding="utf-8") as f:
            return cls.model_validate_json(f.read())
