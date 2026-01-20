#!/usr/bin/env python3
"""
Investigate benchmark instances manually.

For each instance, prints:
- Raw CSV line
- Nano description
- First 75 lines of positive rules
- First 75 lines of negative rules

Usage:
    python investigate_manually.py --instances-csv instances.csv --nr_instances 5
"""

import argparse
import csv
from pathlib import Path


def read_file_lines(file_path: Path, max_lines: int = 15) -> str:
    """
    Read up to max_lines from a file.

    Args:
        file_path: Path to the file to read
        max_lines: Maximum number of lines to read

    Returns:
        String containing the file content (up to max_lines)
    """
    if not file_path.exists():
        return f"[File not found: {file_path}]"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    lines.append(f"... (truncated after {max_lines} lines)")
                    break
                lines.append(line.rstrip())
            return '\n'.join(lines)
    except Exception as e:
        return f"[Error reading file: {e}]"


def investigate_instance(row: dict, base_path: Path, description_type: str) -> None:
    """
    Print investigation information for a single instance.

    Args:
        row: Dictionary from CSV DictReader
        base_path: Base path for the repository (parent of assets/)
        description_type: Type of description to use (e.g., 'nano')
    """
    owner = row['owner']
    repo = row['repo']
    commit_hash = row['commit_hash']
    golden_commit_hash = row['golden_commit_hash']
    combined_score = row.get('combined_score', '')
    category = row['category']
    language = row['language']

    short_hash = commit_hash[:8]

    # Construct paths
    descriptions_dir = base_path / 'assets' / 'descriptions'
    rules_dir = base_path / 'assets' / 'rules'

    nano_desc_path = descriptions_dir / owner / repo / short_hash / f'{description_type}_description.md'
    positive_rules_path = rules_dir / owner / repo / short_hash / 'rules_positive.yml'
    negative_rules_path = rules_dir / owner / repo / short_hash / 'rules_negative.yml'

    # Print CSV line
    print("=" * 80)
    print(f"CSV Line: {owner},{repo},{commit_hash},{golden_commit_hash},{combined_score},{category},{language}")
    print("=" * 80)
    print()

    # Print nano description
    print(f"{description_type.capitalize()} Description:")
    print("-" * 80)
    nano_content = read_file_lines(nano_desc_path, max_lines=999999)  # Read full nano (usually 1 line)
    print(nano_content)
    print()

    # Print first 75 lines of positive rules
    print("First 15 lines of Positive Rules:")
    print("-" * 80)
    positive_content = read_file_lines(positive_rules_path, max_lines=15)
    print(positive_content)
    print()

    # Print first 15 lines of negative rules
    print("First 15 lines of Negative Rules:")
    print("-" * 80)
    negative_content = read_file_lines(negative_rules_path, max_lines=15)
    print(negative_content)
    print()
    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Investigate benchmark instances manually',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        '--instances-csv',
        type=Path,
        required=True,
        help='Path to instances.csv file'
    )

    parser.add_argument(
        '--nr_instances',
        type=int,
        required=True,
        help='Number of instances to investigate'
    )
    parser.add_argument(
        '--description-type',
        type=str,
        default='nano',
        help='Type of description to use (default: nano)'
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.instances_csv.exists():
        print(f"Error: instances.csv not found at {args.instances_csv}")
        return 1

    if args.nr_instances <= 0:
        print(f"Error: --nr_instances must be positive, got {args.nr_instances}")
        return 1

    # Determine base path (find root directory containing 'assets')
    # Start from CSV's parent and walk up until we find the directory containing 'assets'
    base_path = args.instances_csv.parent
    while base_path != base_path.parent:
        if (base_path / 'assets').exists():
            break
        base_path = base_path.parent

    # If we didn't find assets directory, assume current working directory
    if not (base_path / 'assets').exists():
        base_path = Path.cwd()

    # Read and process instances
    with open(args.instances_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader):
            if i >= args.nr_instances:
                break

            investigate_instance(row, base_path, args.description_type)

    print(f"Investigated {min(args.nr_instances, i + 1)} instance(s)")
    return 0


if __name__ == '__main__':
    exit(main())
