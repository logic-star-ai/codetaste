"""Tests for precision metrics calculation tool."""

import json
from pathlib import Path

import pytest

from refactoring_benchmark.coverage.models import Line, SARIFOpengrep, PrecisionMetrics
from refactoring_benchmark.coverage.precision import calculate_precision, _load_precision_data
from refactoring_benchmark.utils.models import InstanceRow


def test_calculate_precision_with_real_data():
    """Test precision metrics calculation with real SARIF and diff data."""
    # Use real data from test assets
    instance_dir = Path("output/go-gitea/gitea/3945c267/claude-code-sonnet-v2.0.76")
    instance_dir = Path("output/go-gitea/gitea/3945c267/null_agent")

    sarif_negative_path = instance_dir / "evaluation/rules_negative.sarif"
    sarif_positive_path = instance_dir / "evaluation/rules_positive.sarif"
    diff_path = instance_dir / "prediction.diff"

    # Skip test if files don't exist
    if not all([sarif_negative_path.exists(), sarif_positive_path.exists(), diff_path.exists()]):
        pytest.skip("Test data files not found")

    # Load precision data (returns PrecisionMetrics with line sets)
    metrics = _load_precision_data(
        sarif_negative_path,
        sarif_positive_path,
        diff_path,
    )
    lines_added = metrics.lines_added
    lines_added_ruled = metrics.lines_matched_by_addition_rules
    for line in lines_added_ruled:
        if line in lines_added:
            pop_line: Line = lines_added.remove(line)
            print(f"Matched added line: {line}")
            assert pop_line.content.strip() in line.content.strip(), f"Content mismatch for line {line}. SARIF content: {repr(line.content[:70])}, Diff content: {repr(pop_line.content[:70])}"

    lines_removed = metrics.lines_removed
    lines_removed_ruled = metrics.lines_matched_by_removal_rules
    for line in lines_removed_ruled:
        if line in lines_removed:
            pop_line: Line = lines_removed.remove(line)
            print(f"Matched removed line: {line}")
            assert pop_line.content.strip() in line.content.strip(), f"Content mismatch for line {line}. SARIF content: {repr(line.content[:70])}, Diff content: {repr(pop_line.content[:70])}"

    # Verify result is PrecisionMetrics object
    assert isinstance(metrics, PrecisionMetrics)

    # Verify all precision values are valid floats between 0 and 1
    assert 0.0 <= metrics.precision_added <= 1.0
    assert 0.0 <= metrics.precision_removed <= 1.0
    assert 0.0 <= metrics.precision_overall <= 1.0


def test_calculate_precision_empty_diff(tmp_path):
    """Test that empty diff returns 0.0 precision."""
    # Create empty SARIF files
    empty_sarif = {
        "version": "2.1.0",
        "runs": []
    }

    sarif_neg_path = tmp_path / "rules_negative.sarif"
    sarif_pos_path = tmp_path / "rules_positive.sarif"

    with open(sarif_neg_path, "w") as f:
        json.dump(empty_sarif, f)

    with open(sarif_pos_path, "w") as f:
        json.dump(empty_sarif, f)

    # Create empty diff
    diff_path = tmp_path / "prediction.diff"
    diff_path.write_text("")

    # Calculate precision metrics
    metrics = calculate_precision(
        sarif_neg_path,
        sarif_pos_path,
        diff_path,
    )

    # Should return 0.0 for all metrics with empty diff
    assert metrics.precision_added == 0.0
    assert metrics.precision_removed == 0.0
    assert metrics.precision_overall == 0.0


def test_calculate_precision_no_intersection(tmp_path):
    """Test precision when SARIF and diff have no overlapping lines."""
    # Create SARIF with results for file1.py line 10
    sarif_with_results = {
        "version": "2.1.0",
        "runs": [{
            "results": [{
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": "file1.py"},
                        "region": {"startLine": 10, "endLine": 10}
                    }
                }]
            }]
        }]
    }

    sarif_neg_path = tmp_path / "rules_negative.sarif"
    sarif_pos_path = tmp_path / "rules_positive.sarif"

    with open(sarif_neg_path, "w") as f:
        json.dump(sarif_with_results, f)

    with open(sarif_pos_path, "w") as f:
        json.dump(sarif_with_results, f)

    # Create diff for file2.py (different file, no overlap)
    diff_content = """diff --git a/file2.py b/file2.py
index 1234567..abcdefg 100644
--- a/file2.py
+++ b/file2.py
@@ -1,1 +1,2 @@
-old line
+new line 1
+new line 2
"""

    diff_path = tmp_path / "prediction.diff"
    diff_path.write_text(diff_content)

    # Calculate precision metrics
    metrics = calculate_precision(
        sarif_neg_path,
        sarif_pos_path,
        diff_path,
    )

    # Should be 0.0 for all metrics since there's no intersection
    assert metrics.precision_added == 0.0
    assert metrics.precision_removed == 0.0
    assert metrics.precision_overall == 0.0


def test_calculate_precision_full_intersection(tmp_path):
    """Test precision when all diff lines are covered by SARIF."""
    # Create SARIF for negative (line 1) and positive (line 2)
    # Note: URIs must match git diff format (a/ and b/ prefixes)
    sarif_neg = {
        "version": "2.1.0",
        "runs": [{
            "results": [{
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": "file1.py"},
                        "region": {"startLine": 1, "endLine": 1}
                    }
                }]
            }]
        }]
    }

    sarif_pos = {
        "version": "2.1.0",
        "runs": [{
            "results": [{
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": "file1.py"},
                        "region": {"startLine": 1, "endLine": 1}
                    }
                }]
            }]
        }]
    }

    sarif_neg_path = tmp_path / "rules_negative.sarif"
    sarif_pos_path = tmp_path / "rules_positive.sarif"

    with open(sarif_neg_path, "w") as f:
        json.dump(sarif_neg, f)

    with open(sarif_pos_path, "w") as f:
        json.dump(sarif_pos, f)

    # Create diff: remove line 1, add line 1
    # Both SARIF files cover line 1, so we get 1 unique covered line
    # Total diff lines = 2 (1 removed + 1 added)
    # Coverage = 1 / 2 = 0.5
    diff_content = """diff --git a/file1.py b/file1.py
index 1234567..abcdefg 100644
--- a/file1.py
+++ b/file1.py
@@ -1,1 +1,1 @@
-old line at line 1
+new line at line 1
"""

    diff_path = tmp_path / "prediction.diff"
    diff_path.write_text(diff_content)

    # Use _load_precision_data to get full PrecisionMetrics
    metrics = _load_precision_data(
        sarif_neg_path,
        sarif_pos_path,
        diff_path,
    )

    # Line.__eq__ compares only uri+line_number+commit
    # So removed line 1 (base commit) and added line 1 (predicted commit) are different
    # Removed: 1 removed line, 1 covered = 1.0
    # Added: 1 added line, 1 covered = 1.0
    # Overall: 2 relevant lines / 2 total diff lines = 1.0
    assert metrics.precision_removed == 1.0
    assert metrics.precision_added == 1.0
    assert metrics.precision_overall == 1.0


def test_calculate_precision_partial_intersection(tmp_path):
    """Test precision with partial overlap between SARIF and diff."""
    # Create SARIF matching only line 2
    sarif_with_results = {
        "version": "2.1.0",
        "runs": [{
            "results": [{
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": "file1.py"},
                        "region": {"startLine": 2, "endLine": 2}
                    }
                }]
            }]
        }]
    }

    empty_sarif = {
        "version": "2.1.0",
        "runs": []
    }

    sarif_neg_path = tmp_path / "rules_negative.sarif"
    sarif_pos_path = tmp_path / "rules_positive.sarif"

    # Only positive SARIF has results
    with open(sarif_neg_path, "w") as f:
        json.dump(empty_sarif, f)

    with open(sarif_pos_path, "w") as f:
        json.dump(sarif_with_results, f)

    # Create diff with 3 added lines (only line 2 matches SARIF)
    diff_content = """diff --git a/file1.py b/file1.py
index 1234567..abcdefg 100644
--- a/file1.py
+++ b/file1.py
@@ -1,0 +1,3 @@
+new line 1
+new line 2
+new line 3
"""

    diff_path = tmp_path / "prediction.diff"
    diff_path.write_text(diff_content)

    # Use _load_precision_data to get full PrecisionMetrics
    metrics = _load_precision_data(
        sarif_neg_path,
        sarif_pos_path,
        diff_path,
    )

    # Removed: 0 removed lines, so 0.0
    # Added: 1 of 3 added lines covered = 1/3 = 0.333...
    # Overall: 1 of 3 total diff lines covered = 1/3 = 0.333...
    assert metrics.precision_removed == 0.0
    assert abs(metrics.precision_added - (1.0 / 3.0)) < 0.001
    assert abs(metrics.precision_overall - (1.0 / 3.0)) < 0.001


def test_instance_row_short_hash():
    """Test that InstanceRow correctly extracts short hash."""
    instance = InstanceRow(
        owner="apache",
        repo="arrow",
        commit_hash="e434536e82ef05430a31556c60d225e90f9382c5",
        golden_commit_hash="df82d4cce52fab5c39b2667e587fa599506b5126",
        category="dependency",
        language="c",
    )

    assert instance.short_hash == "e434536e"
    assert instance.display_path == "apache/arrow/e434536e"
