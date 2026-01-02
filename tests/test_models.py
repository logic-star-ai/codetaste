"""Tests for data models."""
import pytest
from pydantic import ValidationError

from refactoring_benchmark.utils.models import InstanceRow, Metrics, InstanceMetadata


pytestmark = pytest.mark.unit


class TestInstanceRow:
    """Tests for InstanceRow model."""

    def test_valid_instance_row(self):
        """Test creating a valid InstanceRow."""
        row = InstanceRow(
            owner="testowner",
            repo="testrepo",
            golden_commit_hash="abc123def456",
            commit_hash="xyz789",
            category="structural",
            language="python"
        )

        assert row.owner == "testowner"
        assert row.repo == "testrepo"
        assert row.golden_commit_hash == "abc123def456"
        assert row.commit_hash == "xyz789"
        assert row.category == "structural"
        assert row.language == "python"

    def test_instance_row_missing_fields(self):
        """Test that InstanceRow requires all fields."""
        with pytest.raises(ValidationError):
            InstanceRow(
                owner="testowner",
                repo="testrepo"
                # Missing required fields
            )

    def test_instance_row_from_csv_dict(self):
        """Test creating InstanceRow from CSV-like dictionary."""
        csv_data = {
            "owner": "autokey",
            "repo": "autokey",
            "commit_hash": "9309c4fe",
            "golden_commit_hash": "85b948e7",
            "category": "structural",
            "language": "python"
        }

        row = InstanceRow(**csv_data)
        assert row.owner == "autokey"
        assert row.repo == "autokey"


class TestMetrics:
    """Tests for Metrics model."""

    def test_valid_metrics(self):
        """Test creating valid Metrics."""
        metrics = Metrics(
            passed=25,
            failed=2,
            skipped=3,
            total=30
        )

        assert metrics.passed == 25
        assert metrics.failed == 2
        assert metrics.skipped == 3
        assert metrics.total == 30
        assert metrics.error is None

    def test_metrics_with_error(self):
        """Test Metrics with error message."""
        metrics = Metrics(
            passed=0,
            failed=-1,
            skipped=0,
            total=0,
            error="Test execution crashed"
        )

        assert metrics.failed == -1
        assert metrics.error == "Test execution crashed"

    def test_metrics_defaults(self):
        """Test Metrics default values."""
        metrics = Metrics()

        assert metrics.passed == 0
        assert metrics.failed == 0
        assert metrics.skipped == 0
        assert metrics.total == 0
        assert metrics.error is None

    def test_metrics_serialization(self):
        """Test Metrics can be serialized and deserialized."""
        original = Metrics(passed=10, failed=2, skipped=1, total=13)

        # Serialize
        data = original.model_dump()
        assert data["passed"] == 10
        assert data["failed"] == 2

        # Deserialize
        restored = Metrics(**data)
        assert restored.passed == original.passed
        assert restored.failed == original.failed
        assert restored.total == original.total


class TestInstanceMetadata:
    """Tests for InstanceMetadata model."""

    def test_valid_instance_metadata(self):
        """Test creating valid InstanceMetadata."""
        golden_metrics = Metrics(passed=30, failed=0, skipped=0, total=30)
        base_metrics = Metrics(passed=28, failed=2, skipped=0, total=30)

        metadata = InstanceMetadata(
            owner="testowner",
            repo="testrepo",
            golden_metrics=golden_metrics,
            base_metrics=base_metrics,
            base_hash="abc123",
            golden_commit_hash="def456",
            is_success_base=True,
            is_success_golden=True
        )

        assert metadata.owner == "testowner"
        assert metadata.repo == "testrepo"
        assert metadata.base_hash == "abc123"
        assert metadata.golden_commit_hash == "def456"
        assert metadata.is_success_base is True
        assert metadata.is_success_golden is True

    def test_instance_metadata_nested_models(self):
        """Test that InstanceMetadata properly handles nested Metrics models."""
        metadata = InstanceMetadata(
            owner="test",
            repo="test",
            golden_metrics=Metrics(passed=25, failed=5, skipped=0, total=30),
            base_metrics=Metrics(passed=20, failed=10, skipped=0, total=30),
            base_hash="abc",
            golden_commit_hash="def",
            is_success_base=False,
            is_success_golden=True
        )

        # Access nested metrics
        assert metadata.golden_metrics.passed == 25
        assert metadata.base_metrics.passed == 20
        assert isinstance(metadata.golden_metrics, Metrics)
        assert isinstance(metadata.base_metrics, Metrics)

    def test_instance_metadata_serialization(self):
        """Test InstanceMetadata can be serialized to dict."""
        metadata = InstanceMetadata(
            owner="testowner",
            repo="testrepo",
            golden_metrics=Metrics(passed=30, failed=0, skipped=0, total=30),
            base_metrics=Metrics(passed=28, failed=2, skipped=0, total=30),
            base_hash="abc123",
            golden_commit_hash="def456",
            is_success_base=True,
            is_success_golden=True
        )

        # Serialize to dict
        data = metadata.model_dump()

        assert data["owner"] == "testowner"
        assert data["repo"] == "testrepo"
        assert data["golden_metrics"]["passed"] == 30
        assert data["base_metrics"]["passed"] == 28
        assert data["is_success_base"] is True

    def test_instance_metadata_deserialization(self):
        """Test InstanceMetadata can be deserialized from dict."""
        data = {
            "owner": "testowner",
            "repo": "testrepo",
            "golden_metrics": {"passed": 30, "failed": 0, "skipped": 0, "total": 30},
            "base_metrics": {"passed": 28, "failed": 2, "skipped": 0, "total": 30},
            "base_hash": "abc123",
            "golden_commit_hash": "def456",
            "is_success_base": True,
            "is_success_golden": True
        }

        metadata = InstanceMetadata(**data)

        assert metadata.owner == "testowner"
        assert metadata.golden_metrics.passed == 30
        assert metadata.base_metrics.passed == 28

    def test_instance_metadata_all_scenarios(self):
        """Test all four possible success scenarios."""
        # Scenario 1: Both successful (ideal)
        both_success = InstanceMetadata(
            owner="test", repo="test",
            golden_metrics=Metrics(passed=30, failed=0, skipped=0, total=30),
            base_metrics=Metrics(passed=30, failed=0, skipped=0, total=30),
            base_hash="a", golden_commit_hash="b",
            is_success_base=True, is_success_golden=True
        )
        assert both_success.is_success_base and both_success.is_success_golden

        # Scenario 2: Base only
        base_only = InstanceMetadata(
            owner="test", repo="test",
            golden_metrics=Metrics(passed=2, failed=28, skipped=0, total=30),
            base_metrics=Metrics(passed=30, failed=0, skipped=0, total=30),
            base_hash="a", golden_commit_hash="b",
            is_success_base=True, is_success_golden=False
        )
        assert base_only.is_success_base and not base_only.is_success_golden

        # Scenario 3: Golden only
        golden_only = InstanceMetadata(
            owner="test", repo="test",
            golden_metrics=Metrics(passed=30, failed=0, skipped=0, total=30),
            base_metrics=Metrics(passed=2, failed=28, skipped=0, total=30),
            base_hash="a", golden_commit_hash="b",
            is_success_base=False, is_success_golden=True
        )
        assert not golden_only.is_success_base and golden_only.is_success_golden

        # Scenario 4: Both failed
        both_failed = InstanceMetadata(
            owner="test", repo="test",
            golden_metrics=Metrics(passed=0, failed=-1, skipped=0, total=0, error="Crashed"),
            base_metrics=Metrics(passed=0, failed=-1, skipped=0, total=0, error="Crashed"),
            base_hash="a", golden_commit_hash="b",
            is_success_base=False, is_success_golden=False
        )
        assert not both_failed.is_success_base and not both_failed.is_success_golden
