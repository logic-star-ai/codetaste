"""Parse and analyze git diffs and SARIF results."""

import os
from pathlib import Path, PurePosixPath
from typing import Set, Tuple

import whatthepatch
from joblib import Memory

from refactoring_benchmark.coverage.models import Line, SARIFOpengrep

# Cache derived diff metadata to avoid re-reading large files.
cachedir = "./.cache_dir"
memory = Memory(cachedir, verbose=1)

# Standard ignore directories across supported languages (<= 20).
_IGNORE_DIR_NAMES = {
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "target",
    ".gradle",
    "out",
    "bin",
    "obj",
    "vendor",
    ".cache",
    "coverage",
    ".cargo-home",
    "package-lock.json"
}


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def _should_ignore_path(path: str) -> bool:
    parts = PurePosixPath(_normalize_path(path)).parts
    return any(part in _IGNORE_DIR_NAMES for part in parts)


def parse_diff(diff_content: str, base_commit: str, golden_commit: str) -> Tuple[Set[Line], Set[Line]]:
    base_lines: Set[Line] = set()
    golden_lines: Set[Line] = set()
    for diff in whatthepatch.parse_patch(diff_content):
        if not diff.changes:
            continue

        old_path = diff.header.old_path.removeprefix("a/")
        new_path = diff.header.new_path.removeprefix("b/")
        if _should_ignore_path(old_path) or _should_ignore_path(new_path):
            continue

        for old_no, new_no, text, prefix in diff.changes:
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="ignore")
            if old_no is not None and new_no is None:
                base_lines.add(Line(uri=old_path, commit=base_commit, line_number=old_no, content=text))
            elif new_no is not None and old_no is None:
                golden_lines.add(Line(uri=new_path, commit=golden_commit, line_number=new_no, content=text))

    return base_lines, golden_lines


def parse_diff_file(diff_path, base_commit: str, golden_commit: str) -> Tuple[Set[Line], Set[Line]]:
    """Parse a diff file (no caching)."""
    diff_content = Path(diff_path).read_text(errors="replace")
    return parse_diff(diff_content, base_commit, golden_commit)


def parse_diff_line_counts_file(diff_path, base_commit: str, golden_commit: str) -> Tuple[int, int]:
    """Parse a diff file and return (removed_count, added_count), cached by path + mtime."""
    path_str = str(diff_path)
    mtime = os.path.getmtime(diff_path)
    nr_lines_removed, nr_lines_added = _cached_parse_diff_line_counts_file(path_str, mtime, base_commit, golden_commit)
    if nr_lines_removed + nr_lines_added > 50000:
        print(f"Warning: Diff file {diff_path} has {nr_lines_removed} removed and {nr_lines_added} added lines, which may indicate an unusually large change or a parsing issue.")
    return nr_lines_removed, nr_lines_added


@memory.cache
def _cached_parse_diff_line_counts_file(
    path_str: str, mtime: float, base_commit: str, golden_commit: str
) -> Tuple[int, int]:
    lines_removed, lines_added = parse_diff_file(path_str, base_commit, golden_commit)
    return len(lines_removed), len(lines_added)


def _lines_from_locations(locations: list, commit: str) -> Set[Line]:
    lines: Set[Line] = set()

    for location in locations:
        # Extract physical location
        phys_loc = location.get("physicalLocation")
        if not phys_loc:
            continue

        # Extract file URI
        artifact = phys_loc.get("artifactLocation")
        if not artifact or "uri" not in artifact:
            continue
        uri = artifact["uri"]

        # Extract region (line range)
        region = phys_loc.get("region")
        if not region:
            continue

        start_line = region.get("startLine")
        end_line = region.get("endLine", start_line)

        if start_line is None:
            continue

        # Extract snippet text if available
        snippet = region.get("snippet", {})
        snippet_text = snippet.get("text", "") if isinstance(snippet, dict) else ""

        if snippet_text is not None and len(snippet_text.splitlines()) == end_line - start_line + 1:
            for line_num, line_text in zip(range(start_line, end_line + 1), snippet_text.splitlines()):
                lines.add(Line(uri=uri, commit=commit, line_number=line_num, content=line_text))
        else:
            for line_num in range(start_line, end_line + 1):
                lines.add(Line(uri=uri, commit=commit, line_number=line_num, content=snippet_text))

    return lines


def parse_sarif(sarif: SARIFOpengrep, commit: str) -> Set[Line]:
    """
    Extract matched lines from SARIF results.

    Args:
        sarif: Parsed SARIF data
        commit: The commit hash these results correspond to

    Returns:
        Set of Line objects representing all lines matched in SARIF results
    """
    lines: Set[Line] = set()

    for run in sarif.runs:
        if not run.results:
            continue

        for result in run.results:
            if not result.locations:
                continue
            lines.update(_lines_from_locations(result.locations, commit))

    return lines


def parse_sarif_by_rule(sarif: SARIFOpengrep, commit: str) -> dict[str, Set[Line]]:
    """
    Extract matched lines grouped by rule ID.

    Args:
        sarif: Parsed SARIF data
        commit: The commit hash these results correspond to

    Returns:
        Dict of rule_id -> set of Line objects matched by that rule
    """
    lines_by_rule: dict[str, Set[Line]] = {}

    for run in sarif.runs:
        if not run.results:
            continue

        for result in run.results:
            if not result.locations:
                continue
            rule_id = result.ruleId
            if not rule_id:
                continue
            clean_id = rule_id.split(".")[-1]
            lines_by_rule.setdefault(clean_id, set()).update(_lines_from_locations(result.locations, commit))

    return lines_by_rule
