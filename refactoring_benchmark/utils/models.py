"""Pydantic models for data validation and type safety."""

import os
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

    @property
    def short_hash(self) -> str:
        """First 8 characters of commit hash."""
        return self.commit_hash[:8]

    @property
    def id(self) -> str:
        """Instance ID: {owner}__{repo}-{short_hash}"""
        return f"{self.owner}__{self.repo}-{self.short_hash}".lower()

    @property
    def image_identifier(self) -> str:
        """Docker image base: localhost/benchmark/{id}"""
        return f"localhost/benchmark/{self.id}"

    @property
    def setup_image(self) -> str:
        """Setup image name: {image_identifier}__setup"""
        return f"{self.image_identifier}__setup"

    @property
    def runtime_image(self) -> str:
        """Runtime image name: {image_identifier}__runtime"""
        return f"{self.image_identifier}__runtime"

    @property
    def display_path(self) -> str:
        """Display path: {owner}/{repo}/{short_hash}"""
        return f"{self.owner}/{self.repo}/{self.short_hash}"

    def instance_dir(self, base_path: str = "instance_images") -> str:
        """Instance directory: {base_path}/{owner}/{repo}/{short_hash}"""
        return os.path.join(base_path, self.owner, self.repo, self.short_hash)

    def asset_dir(self, asset_type: str, base_path: str = "assets") -> str:
        """Asset directory: {base_path}/{asset_type}/{owner}/{repo}/{short_hash}"""
        return os.path.join(
            base_path, asset_type, self.owner, self.repo, self.short_hash
        )


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
        return (
            self.error is None
            and self.total >= 10
            and (self.passed / self.total) >= 0.3
        )


class InstanceMetadata(BaseModel):
    """Complete metadata for a benchmark instance."""

    owner: str
    repo: str
    golden_metrics: Metrics
    base_metrics: Metrics
    base_hash: str
    golden_commit_hash: str

    @property
    def is_success_base(self) -> bool:
        """Indicating if tests appear to be running correctly on base."""
        return self.base_metrics.is_valid

    @property
    def is_success_golden(self) -> bool:
        """Indicating if tests appear to be running correctly on golden."""
        return self.golden_metrics.is_valid

    @property
    def setup_quality(
        self,
    ) -> Literal["both_valid", "only_base_valid", "only_golden_valid", "neither_valid"]:
        """Classify setup quality based on test metrics validity."""
        base_valid = self.is_success_base
        golden_valid = self.is_success_golden
        if base_valid and golden_valid:
            return "both_valid"
        elif base_valid and not golden_valid:
            return "only_base_valid"
        elif not base_valid and golden_valid:
            return "only_golden_valid"
        else:
            return "neither_valid"
