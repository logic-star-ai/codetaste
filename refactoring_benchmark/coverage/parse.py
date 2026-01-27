"""Parse and analyze git diffs and SARIF results."""
import whatthepatch

from refactoring_benchmark.coverage.models import Line, SARIFOpengrep


from typing import Set, Tuple

def parse_diff(diff_content: str, base_commit: str, golden_commit: str) -> Tuple[Set[Line], Set[Line]]:
    base_lines: Set[Line] = set()
    golden_lines: Set[Line] = set()
    for diff in whatthepatch.parse_patch(diff_content):
        if not diff.changes:
            continue
            
        old_path = diff.header.old_path
        new_path = diff.header.new_path

        for old_no, new_no, text, prefix in diff.changes:
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="ignore")
            if old_no is not None and new_no is None:
                base_lines.add(Line(
                    uri=old_path, 
                    commit=base_commit, 
                    line_number=old_no, 
                    content=text
                ))
            elif new_no is not None and old_no is None:
                golden_lines.add(Line(
                    uri=new_path, 
                    commit=golden_commit, 
                    line_number=new_no, 
                    content=text
                ))
                
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
