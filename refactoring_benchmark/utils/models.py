"""Pydantic models for data validation and type safety."""
from pydantic import BaseModel
from typing import Literal, Optional, Dict


class InstanceRow(BaseModel):
    """Represents a single row from the instances CSV file."""
    owner: str
    repo: str
    golden_commit_hash: str
    commit_hash: str
    category: str
    language: str


class Metrics(BaseModel):
    """Test execution metrics."""
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    total: int = 0
    error: Optional[str] = None


class InstanceMetadata(BaseModel):
    """Complete metadata for a benchmark instance."""
    owner: str
    repo: str
    golden_metrics: Metrics
    start_metrics: Metrics
    base_hash: str
    golden_commit_hash: str
    is_success_base: bool # Indicating if tests appear to be running correctly on base
    is_success_golden: bool
