"""Tests for diff parsing and analysis."""

import json
from pathlib import Path
from refactoring_benchmark.coverage.parse import parse_diff, parse_sarif
from refactoring_benchmark.coverage.models import SARIFOpengrep


def test_parse_diff_line_count():
    """Test that parse_diff captures all changed lines from the diff."""
    # Load the diff file
    diff_path = Path("assets/diffs/99designs/gqlgen/d5c9f896/golden.diff")
    diff_content = diff_path.read_text()

    # Count lines starting with "-" or "+" (excluding file markers "---" and "+++")
    expected_count = 0
    for line in diff_content.split("\n"):
        if line.startswith("-") and not line.startswith("---"):
            expected_count += 1
        elif line.startswith("+") and not line.startswith("+++"):
            expected_count += 1

    # Parse the diff
    base_commit = "d5c9f896"  # Short hash from the path
    golden_commit = "golden"  # Placeholder
    base_lines, golden_lines = parse_diff(diff_content, base_commit, golden_commit)

    # The total number of Line objects should equal the number of changed lines
    actual_count = len(base_lines) + len(golden_lines)

    assert actual_count == expected_count, (
        f"Expected {expected_count} total changed lines, but got {actual_count} "
        f"(base: {len(base_lines)}, golden: {len(golden_lines)})"
    )


def test_parse_sarif_extracts_lines():
    """Test that parse_sarif correctly extracts lines from SARIF results."""
    # Load SARIF file
    sarif_path = Path("outputs/pseudo_agents/direct/apache/arrow/e434536e/golden_agent/evaluation/rules_positive.sarif")
    with open(sarif_path) as f:
        raw_data = json.load(f)

    sarif = SARIFOpengrep.model_validate(raw_data)
    lines = parse_sarif(sarif, "e434536e")

    # Verify lines were extracted
    assert len(lines) > 0, "Should extract at least one line from SARIF"

    # Verify Line structure
    first_line = next(iter(lines))
    assert first_line.uri, "Line should have a URI"
    assert first_line.commit == "e434536e", "Line should have correct commit"
    assert first_line.line_number > 0, "Line should have positive line number"

    # Verify all lines have valid structure
    for line in lines:
        assert line.uri, f"Line missing URI: {line}"
        assert line.commit, f"Line missing commit: {line}"
        assert line.line_number > 0, f"Line has invalid line_number: {line}"


def test_parse_sarif_negative_and_diff_intersection():
    """Test computing intersection between SARIF negative results and diff lines."""
    # Load SARIF negative results
    sarif_path = Path("outputs/pseudo_agents/direct/apache/arrow/e434536e/null_agent/evaluation/rules_negative.sarif")
    with open(sarif_path) as f:
        sarif_data = json.load(f)

    sarif = SARIFOpengrep.model_validate(sarif_data)
    sarif_lines = parse_sarif(sarif, "e434536e")

    # Load diff
    diff_path = Path("outputs/pseudo_agents/direct/apache/arrow/e434536e/golden_agent/prediction.diff")
    diff_content = diff_path.read_text()
    _, golden_lines = parse_diff(diff_content, "e434536e", "predicted")

    # Compute intersection with golden lines (added/modified lines in prediction)
    intersection = sarif_lines & golden_lines

    # Verify results
    assert len(sarif_lines) > 0, "SARIF should have extracted lines"
    assert len(golden_lines) > 0, "Diff should have golden lines"

    print(f"\nSARIF negative lines: {len(sarif_lines)}")
    print(f"Diff golden lines: {len(golden_lines)}")
    print(f"Intersection: {len(intersection)}")

    # Show sample intersection if any
    if intersection:
        sample = sorted(intersection, key=lambda x: (x.uri, x.line_number))[:3]
        print("\nSample intersection lines:")
        for line in sample:
            print(f"  {line.uri}:{line.line_number}")
