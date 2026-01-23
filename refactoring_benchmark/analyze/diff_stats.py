import os

from pydantic import BaseModel


class DiffStat(BaseModel):
    """Statistics about a diff: number of added and removed lines."""

    added_lines: int = 0
    removed_lines: int = 0

def parse_diff_stats(diff_input, exclude_exts=None):
    """
    Parses a git-style diff and counts added/removed lines.
    :param diff_input: An iterable of strings (e.g., a file object or list of lines).
    :param exclude_exts: A set of extensions to skip (e.g., {'.md', '.txt', ''}).
    """
    if exclude_exts is None:
        exclude_exts = {'.md', '.txt', ''}
    
    total_added = 0
    total_removed = 0
    skip_file = False

    for line in diff_input:
        if line.startswith('diff --git'):
            parts = line.split(' ')
            if len(parts) >= 4:
                b_path = parts[3].replace('b/', '', 1)
                _, ext = os.path.splitext(b_path)
                skip_file = ext.lower() in exclude_exts
            else:
                skip_file = False
            continue

        if "GIT binary patch" in line:
            skip_file = True
            continue

        # 3. Skip if we are in an excluded file or binary blob
        if skip_file:
            continue
        if line.startswith('+') and not line.startswith('+++'):
            total_added += 1
        elif line.startswith('-') and not line.startswith('---'):
            total_removed += 1

    return DiffStat(added_lines=total_added, removed_lines=total_removed)

def parse_diff_file(diff_file_path, exclude_exts=None) -> DiffStat:
    """Parse a diff file to get added and removed line statistics."""
    with open(diff_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return parse_diff_stats(f, exclude_exts=exclude_exts)