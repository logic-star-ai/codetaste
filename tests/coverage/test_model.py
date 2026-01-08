import json
from pathlib import Path
import pytest
from refactoring_benchmark.coverage.models import SARIFOpengrep


@pytest.fixture
def sarif_file_path():
    """Path to a sample SARIF file for testing."""
    return Path("output/apache/arrow/e434536e/claude-code-sonnet-v2.0.76/evaluation/rules_positive.sarif")


def test_sarif_opengrep_model_loads_and_preserves_structure(sarif_file_path):
    """Test that SARIFOpengrep correctly loads a SARIF file without data loss."""
    # Load raw JSON
    with open(sarif_file_path) as f:
        raw_data = json.load(f)

    # Parse with Pydantic model - should not raise validation errors
    sarif = SARIFOpengrep.model_validate(raw_data)

    # Dump back to dict with by_alias to get $schema back
    dumped_data = sarif.model_dump(by_alias=True, exclude_none=True)

    # Verify critical keys are preserved
    assert dumped_data["version"] == raw_data["version"]
    assert len(dumped_data["runs"]) == len(raw_data["runs"])

    # Verify schema is preserved
    if "$schema" in raw_data:
        assert dumped_data.get("$schema") == raw_data["$schema"]

    # Verify run structure
    if raw_data["runs"]:
        raw_run = raw_data["runs"][0]
        dumped_run = dumped_data["runs"][0]

        # Check invocations preserved
        if "invocations" in raw_run:
            assert len(dumped_run["invocations"]) == len(raw_run["invocations"])

        # Check results preserved with structure validation
        if "results" in raw_run and raw_run["results"]:
            assert len(dumped_run["results"]) == len(raw_run["results"])

            # Verify first result has expected structure
            raw_result = raw_run["results"][0]
            dumped_result = dumped_run["results"][0]

            for key in ["ruleId", "message", "locations"]:
                if key in raw_result:
                    assert key in dumped_result, f"Key '{key}' lost in result"
