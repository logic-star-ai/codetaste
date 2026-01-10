#!/usr/bin/env python3
"""
Create files_description.md for all instances based on golden diff analysis.

For each instance, parses the golden diff to identify the most frequently
modified files and generates a files_description.md file that guides agents
to focus on those concerning files.
"""

import csv
from collections import Counter
from pathlib import Path
from typing import List, Tuple

from refactoring_benchmark.coverage.parse import parse_diff


DESCRIPTION_TEMPLATE = """Autonomously identify and execute improvements to the **entire** codebase. Optimize structure, architecture, code quality and/or logic flow. Proceed directly to modifying the actual codebase; do not output analysis, plan, roadmap or similar files.
Some of the files that look particularly concerning to me are the following:
{file_list}"""


def parse_golden_diff_files(diff_path: Path, commit_hash: str, golden_commit_hash: str) -> List[Tuple[str, int]]:
    """
    Parse a golden diff and return the top files by line change frequency.

    Args:
        diff_path: Path to the golden.diff file
        commit_hash: Base commit hash
        golden_commit_hash: Golden commit hash

    Returns:
        List of (uri, count) tuples sorted by count descending
    """
    if not diff_path.exists():
        return []

    # Read diff content
    diff_content = diff_path.read_text(encoding="utf-8")

    # Parse diff to get base and golden lines
    base_lines, golden_lines = parse_diff(diff_content, commit_hash, golden_commit_hash)

    # Count URI occurrences in golden lines (added lines)
    uri_counter = Counter(line.uri for line in golden_lines)

    # Return sorted by frequency (descending)
    return uri_counter.most_common()


def create_files_description(top_files: List[Tuple[str, int]], max_files: int = 25) -> str:
    """
    Create the files_description.md content from a list of files.

    Args:
        top_files: List of (uri, count) tuples
        max_files: Maximum number of files to include

    Returns:
        Formatted description content
    """
    # Take top N files
    selected_files = top_files[:max_files]

    # Format as bullet list
    file_list = "\n".join(f"- {uri}" for uri, _ in selected_files)

    return DESCRIPTION_TEMPLATE.format(file_list=file_list)


def create_files_descriptions(
    instances_csv: Path, diffs_dir: Path, descriptions_dir: Path, max_files: int = 25
) -> None:
    """
    Create files_description.md for all instances.

    Args:
        instances_csv: Path to instances.csv
        diffs_dir: Path to assets/diffs directory
        descriptions_dir: Path to assets/descriptions directory
        max_files: Maximum number of files to include in each description
    """
    success_count = 0
    error_count = 0
    skip_count = 0

    with open(instances_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            owner = row["owner"]
            repo = row["repo"]
            commit_hash = row["commit_hash"]
            golden_commit_hash = row["golden_commit_hash"]
            short_hash = commit_hash[:8]

            # Source: golden.diff
            diff_path = diffs_dir / owner / repo / short_hash / "golden.diff"

            if not diff_path.exists():
                print(f"⊗ Skipped (no diff): {owner}/{repo}/{short_hash}")
                skip_count += 1
                continue

            try:
                # Parse golden diff to get top files
                top_files = parse_golden_diff_files(diff_path, commit_hash, golden_commit_hash)

                if not top_files:
                    print(f"⊗ Skipped (no files): {owner}/{repo}/{short_hash}")
                    skip_count += 1
                    continue

                # Create description content
                description_content = create_files_description(top_files, max_files)

                # Target directory
                target_dir = descriptions_dir / owner / repo / short_hash
                target_dir.mkdir(parents=True, exist_ok=True)

                # Write files_description.md
                output_path = target_dir / "files_description.md"
                output_path.write_text(description_content, encoding="utf-8")

                print(
                    f"✓ Created: {output_path} ({len(top_files)} files found, top {min(len(top_files), max_files)} included)"
                )
                success_count += 1

            except Exception as e:
                print(f"✗ Error processing {owner}/{repo}/{short_hash}: {e}")
                error_count += 1

    print(f"\nSummary:")
    print(f"  Success: {success_count}")
    print(f"  Skipped: {skip_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total: {success_count + skip_count + error_count}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create files_description.md for all instances based on golden diff analysis.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path(__file__).parent.parent.parent / "instances.csv",
        help="Path to instances.csv (default: ./instances.csv)",
    )

    parser.add_argument(
        "--diffs-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "assets" / "diffs",
        help="Path to diffs directory (default: ./assets/diffs)",
    )

    parser.add_argument(
        "--descriptions-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "assets" / "descriptions",
        help="Path to descriptions directory (default: ./assets/descriptions)",
    )

    parser.add_argument(
        "--max-files",
        type=int,
        default=25,
        help="Maximum number of files to include in each description (default: 25)",
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.instances_csv.exists():
        print(f"Error: instances.csv not found at {args.instances_csv}")
        return 1

    if not args.diffs_dir.exists():
        print(f"Error: diffs directory not found at {args.diffs_dir}")
        return 1

    if not args.descriptions_dir.exists():
        print(f"Error: descriptions directory not found at {args.descriptions_dir}")
        return 1

    print("Creating files_description.md files...")
    print(f"  Instances CSV: {args.instances_csv}")
    print(f"  Diffs dir: {args.diffs_dir}")
    print(f"  Descriptions dir: {args.descriptions_dir}")
    print(f"  Max files per description: {args.max_files}")
    print()

    create_files_descriptions(args.instances_csv, args.diffs_dir, args.descriptions_dir, args.max_files)
    return 0


if __name__ == "__main__":
    exit(main())
