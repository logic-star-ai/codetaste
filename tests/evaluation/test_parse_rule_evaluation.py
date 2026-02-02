"""Tests for parse_rule_evaluation function."""

import json
from pathlib import Path
from refactoring_benchmark.evaluation.parser import parse_rule_evaluation


import json
import pytest
from pathlib import Path
from refactoring_benchmark.evaluation.parser import parse_rule_evaluation

@pytest.fixture
def evaluation_assets():
    """Fixture to provide asset paths and ensure cleanup before/after tests."""
    asset_dir = Path(__file__).parent / "assets" / "parse_rule_evaluation"
    reports = [
        asset_dir / "rules_positive_report.json",
        asset_dir / "rules_negative_report.json"
    ]
    
    # Pre-test cleanup: ensure a fresh state
    for report in reports:
        report.unlink(missing_ok=True)
        
    yield asset_dir, reports

    # Post-test cleanup: remove files created during the test
    for report in reports:
        report.unlink(missing_ok=True)


def test_parse_rule_evaluation(evaluation_assets):
    """Test parsing rule evaluation from real SARIF and YAML files."""
    asset_dir, _ = evaluation_assets
    result = parse_rule_evaluation(asset_dir)

    # Verify counts match expected values from null_agent
    assert result.total_positive_rules == 85
    assert result.total_negative_rules == 52
    assert result.positive_rules_matched == 0
    assert result.negative_rules_matched == 52

    # Verify computed metrics
    assert result.positive_ifr == 0.0
    assert result.negative_ifr == 0.0
    assert result.ifr == 0.0


def test_parse_rule_evaluation_creates_reports(evaluation_assets):
    """Test that parse_rule_evaluation creates JSON report files."""
    asset_dir, (pos_report, neg_report) = evaluation_assets

    parse_rule_evaluation(asset_dir)

    # Verify reports were created
    assert pos_report.exists()
    assert neg_report.exists()

    # Verify report structure
    pos_data = json.loads(pos_report.read_text())
    neg_data = json.loads(neg_report.read_text())

    assert isinstance(pos_data, dict)
    assert isinstance(neg_data, dict)
    # null_agent matched no positive rules
    assert len([r for r in pos_data if pos_data[r] > 0]) == 0
    # all negative rules matched
    assert len([r for r in neg_data if neg_data[r] > 0]) == 52
