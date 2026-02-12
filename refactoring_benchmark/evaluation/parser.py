"""Parsing utilities for evaluation outputs."""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple

import yaml

from refactoring_benchmark.bootstrap.models import ExecutionInstanceMetadata
from refactoring_benchmark.evaluation.models import (RuleMetrics,
                                                     SingleRuleResult,
                                                     TestMetrics)


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
    for i, line in enumerate(reversed(lines)):
        if i == 10:
            break
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            return TestMetrics(**data)
        except (json.JSONDecodeError, ValueError, TypeError):
            continue

    return None


def parse_sarif_file(sarif_path: Path, rules_path: Path) -> Tuple[int, int, Dict[str, SingleRuleResult]]:
    """
    Parse SARIF file and count rule matches.
    """
    total_rules = 0
    rules_data = {}
    if rules_path.exists():
        try:
            with open(rules_path, "r") as f:
                rules_data = yaml.safe_load(f)
            if "rules" in rules_data:
                total_rules = len(rules_data["rules"])
        except Exception:
            pass

    # Count matches from SARIF
    rules_matched_dict = {
        r["id"].split(".")[-1]: SingleRuleResult(**r, golden_matched=r["metadata"]["nr_refactored_patterns"])
        for r in rules_data.get("rules", [])
    }

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
                                if clean_id in rules_matched_dict:
                                    rules_matched_dict[clean_id].prediction_matched += 1
        except Exception:
            pass

    rules_matched = len([r for r in rules_matched_dict if rules_matched_dict[r].prediction_matched > 0])
    return rules_matched, total_rules, rules_matched_dict


def parse_rule_evaluation(eval_dir: Path, create_report: bool = False) -> RuleMetrics:
    """
    Parse rule evaluation results from SARIF and YAML files.
    """
    sarif_pos = eval_dir / "rules_positive.sarif"
    sarif_neg = eval_dir / "rules_negative.sarif"
    rules_pos = eval_dir / "rules_positive.yml"
    rules_neg = eval_dir / "rules_negative.yml"

    pos_matched, pos_total, pos_matched_dict = parse_sarif_file(sarif_pos, rules_pos)
    neg_matched, neg_total, neg_matched_dict = parse_sarif_file(sarif_neg, rules_neg)

    if create_report:
        with open(eval_dir / "rules_positive_report.json", "w") as f:
            json.dump({k: v.model_dump() for k, v in pos_matched_dict.items()}, f, indent=2)
        with open(eval_dir / "rules_negative_report.json", "w") as f:
            json.dump({k: v.model_dump() for k, v in neg_matched_dict.items()}, f, indent=2)

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
