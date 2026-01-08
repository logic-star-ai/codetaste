"""Parse and analyze git diffs and SARIF results."""

import re
from typing import Set, Tuple

from refactoring_benchmark.coverage.models import Line, SARIFOpengrep


def parse_diff(diff_content: str, base_commit: str, golden_commit: str) -> Tuple[Set[Line], Set[Line]]:
    """
    Parse a git diff and extract changed lines for both commits.

    Args:
        diff_content: The git diff content as a string
        base_commit: The base commit hash
        golden_commit: The golden commit hash

    Returns:
        A tuple of (base_lines, golden_lines) where:
        - base_lines: Set of Line objects representing removed/changed lines from base
        - golden_lines: Set of Line objects representing added/changed lines from golden
    """
    base_lines: Set[Line] = set()
    golden_lines: Set[Line] = set()

    current_file = None  # New/target file path (for golden lines)
    old_file = None  # Old/source file path (for base lines, used in renames)
    old_line_num = 0
    new_line_num = 0

    lines = diff_content.split("\n")

    for line in lines:
        # Match file headers: diff --git a/path b/path
        if line.startswith("diff --git"):
            # Extract file path from "diff --git a/path b/path"
            match = re.search(r"b/(.+)$", line)
            if match:
                current_file = match.group(1)
                old_file = current_file  # Default: old and new are same
            continue

        # Handle renames: "rename from old/path"
        if line.startswith("rename from "):
            old_file = line[len("rename from "):]
            continue

        # Handle renames: "rename to new/path"
        if line.startswith("rename to "):
            current_file = line[len("rename to "):]
            continue

        # Match hunk headers: @@ -10,5 +10,6 @@
        if line.startswith("@@"):
            match = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if match:
                old_line_num = int(match.group(1))
                new_line_num = int(match.group(2))
            continue

        # Skip other metadata lines
        if line.startswith("---") or line.startswith("+++") or line.startswith("index"):
            continue

        # If we don't have file paths, skip
        if current_file is None or old_file is None:
            continue

        # Process diff lines
        if line.startswith("-") and not line.startswith("---"):
            # Line removed from base commit (strip the leading '-')
            # Use old_file for base lines (handles renames correctly)
            content = line[1:] if len(line) > 1 else ""
            base_lines.add(Line(uri=old_file, commit=base_commit, line_number=old_line_num, content=content))
            old_line_num += 1

        elif line.startswith("+") and not line.startswith("+++"):
            # Line added in golden commit (strip the leading '+')
            # Use current_file for golden lines (the new/target path)
            content = line[1:] if len(line) > 1 else ""
            golden_lines.add(Line(uri=current_file, commit=golden_commit, line_number=new_line_num, content=content))
            new_line_num += 1

        elif line.startswith(" "):
            # Context line (unchanged) - increment both counters
            old_line_num += 1
            new_line_num += 1

        # Empty lines or other content - treat as context
        elif not line.startswith("\\"):  # Skip "\ No newline at end of file"
            if line == "":
                old_line_num += 1
                new_line_num += 1

    return base_lines, golden_lines


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

            for location in result.locations:
                # Extract physical location
                phys_loc = location.get('physicalLocation')
                if not phys_loc:
                    continue

                # Extract file URI
                artifact = phys_loc.get('artifactLocation')
                if not artifact or 'uri' not in artifact:
                    continue
                uri = artifact['uri']

                # Extract region (line range)
                region = phys_loc.get('region')
                if not region:
                    continue

                start_line = region.get('startLine')
                end_line = region.get('endLine', start_line)

                if start_line is None:
                    continue

                # Extract snippet text if available
                snippet = region.get('snippet', {})
                snippet_text = snippet.get('text', '') if isinstance(snippet, dict) else ''
                
                if snippet_text is not None and len(snippet_text.splitlines()) == end_line - start_line + 1:
                    for line_num, line_text in zip(range(start_line, end_line + 1), snippet_text.splitlines()):
                        lines.add(Line(uri=uri, commit=commit, line_number=line_num, content=line_text))
                else:
                    for line_num in range(start_line, end_line + 1):
                        lines.add(Line(uri=uri, commit=commit, line_number=line_num, content=snippet_text))

    return lines
