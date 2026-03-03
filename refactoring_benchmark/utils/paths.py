"""Shared filesystem paths for the repository."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PSEUDO_AGENTS_DIR = REPO_ROOT / "outputs" / "pseudo_agents" / "direct"
BASELINE_RESULTS_DIR = REPO_ROOT / "baseline_results"
