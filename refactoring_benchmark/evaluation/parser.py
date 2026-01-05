"""Parsing utilities for evaluation outputs."""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple

import yaml

from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata
from refactoring_benchmark.evaluation.models import RuleMetrics, TestMetrics


def parse_test_output(stdout: str) -> Optional[TestMetrics]:
    """
    Parse test metrics from container stdout.

    The container outputs JSON on the last line with test results.

    Args:
        stdout: Complete stdout from test evaluation container

    Returns:
        TestMetrics if successfully parsed, None otherwise
    """
    if not stdout or not stdout.strip():
        return None

    # Try to parse from last line backwards (container may output JSON at end)
    lines = stdout.strip().split("\n")
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            return TestMetrics(**data)
        except (json.JSONDecodeError, ValueError):
            continue

    return None


def parse_sarif_file(sarif_path: Path, rules_path: Path) -> Tuple[int, int]:
    """
    Parse SARIF file and count rule matches.

    Args:
        sarif_path: Path to SARIF output file
        rules_path: Path to rules YAML file (for total count)

    Returns:
        Tuple of (rules_matched, total_rules)
    """
    # Get total rules from YAML
    total_rules = 0
    if rules_path.exists():
        try:
            with open(rules_path, "r") as f:
                rules_data = yaml.safe_load(f)
            if "rules" in rules_data:
                total_rules = len(rules_data["rules"])
        except Exception:
            pass

    # Count matches from SARIF
    rules_matched_set = set()
    if sarif_path.exists():
        try:
            with open(sarif_path, "r") as f:
                sarif_data = json.load(f)

            if "runs" in sarif_data:
                for run in sarif_data["runs"]:
                    if "results" in run:
                        for result in run["results"]:
                            rule_id = result.get("ruleId")
                            if rule_id:
                                # Clean rule ID (remove prefix)
                                clean_id = rule_id.split(".")[-1]
                                rules_matched_set.add(clean_id)
        except Exception:
            pass

    rules_matched = len(rules_matched_set)
    return rules_matched, total_rules


def parse_rule_evaluation(eval_dir: Path) -> RuleMetrics:
    """
    Parse rule evaluation results from SARIF and YAML files.

    Args:
        eval_dir: Evaluation directory containing SARIF and YAML files

    Returns:
        RuleMetrics with counts for positive and negative rules
    """
    sarif_pos = eval_dir / "rules_positive.sarif"
    sarif_neg = eval_dir / "rules_negative.sarif"
    rules_pos = eval_dir / "rules_positive.yml"
    rules_neg = eval_dir / "rules_negative.yml"

    pos_matched, pos_total = parse_sarif_file(sarif_pos, rules_pos)
    neg_matched, neg_total = parse_sarif_file(sarif_neg, rules_neg)

    return RuleMetrics(
        positive_rules_matched=pos_matched,
        negative_rules_matched=neg_matched,
        total_positive_rules=pos_total,
        total_negative_rules=neg_total,
    )


def load_instance_metadata(metadata_path: Path) -> ExecutionInstanceMetadata:
    """
    Load instance metadata from JSON file.

    Args:
        metadata_path: Path to instance_metadata.json

    Returns:
        ExecutionInstanceMetadata instance

    Raises:
        FileNotFoundError: If metadata file doesn't exist
        ValueError: If metadata is invalid
    """
    if not metadata_path.exists():
        raise FileNotFoundError(f"Instance metadata not found: {metadata_path}")

    try:
        with open(metadata_path, "r") as f:
            data = json.load(f)
        return ExecutionInstanceMetadata(**data)
    except Exception as e:
        raise ValueError(f"Invalid instance metadata: {e}")
