"""Data models for bootstrap configuration."""

from pathlib import Path
from pydantic import BaseModel, Field


class BootstrapConfig(BaseModel):
    """Runtime configuration for bootstrap execution."""

    instances_csv: Path
    nr_workers: int = Field(gt=0, default=4)
    force_runtime_build: bool = False
    api_key: str
    base_image: str = "benchmark/benchmark-base-all"
    timeout_bootstrap: int = Field(gt=0, default=7200)  # 2 hours
    supported_languages: list[str] = Field(
        default_factory=lambda: ["python", "javascript", "java", "c", "go", "rust"]
    )

    class Config:
        arbitrary_types_allowed = True
