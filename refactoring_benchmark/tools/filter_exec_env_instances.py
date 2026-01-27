#!/usr/bin/env python3
"""
Filter instances CSV to only include instances with valid execution environments.

Reads instances.csv and outputs instances_exec_env.csv containing only instances
where instance_metadata.json exists and has_execution_environment is true.

Preserves all columns from the original CSV file.
"""

import argparse
import csv
import json
from pathlib import Path

from refactoring_benchmark.utils.models import InstanceRow


def has_valid_execution_environment(
    owner: str, repo: str, commit_hash: str, instance_images_dir: Path
) -> bool:
    """
    Check if an instance has a valid execution environment.

    Args:
        owner: Repository owner
        repo: Repository name
        commit_hash: Commit hash
        instance_images_dir: Base directory for instance images

    Returns:
        True if instance_metadata.json exists and has_execution_environment is true
    """
    short_hash = commit_hash[:8]
    metadata_path = (
        instance_images_dir
        / owner
        / repo
        / short_hash
        / "instance_metadata.json"
    )

    if not metadata_path.exists():
        return False

    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
            return metadata.get("has_execution_environment", False) is True
    except (json.JSONDecodeError, IOError):
        return False


def write_instances_csv(rows: list[dict], fieldnames: list[str], output_path: Path) -> None:
    """
    Write instance rows to CSV file.

    Args:
        rows: List of row dictionaries to write
        fieldnames: Column names for CSV
        output_path: Path to output CSV file
    """
    if not rows:
        print("Warning: No instances to write")
        return

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(
        description="Filter instances.csv to only include instances with valid execution environments.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path(__file__).parent.parent.parent / "instances.csv",
        help="Path to input instances CSV file",
    )

    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path(__file__).parent.parent.parent / "instances_exec_env.csv",
        help="Path to output filtered CSV file",
    )

    parser.add_argument(
        "--instance-images-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "instance_images",
        help="Base directory for instance images",
    )

    args = parser.parse_args()

    # Resolve paths
    instances_csv = args.instances_csv.resolve()
    output_csv = args.output_csv.resolve()
    instance_images_dir = args.instance_images_dir.resolve()

    # Validate inputs
    if not instances_csv.exists():
        print(f"Error: instances.csv not found at {instances_csv}")
        return 1

    if not instance_images_dir.exists():
        print(f"Error: instance_images directory not found at {instance_images_dir}")
        return 1

    # Load instances from CSV (as raw dictionaries to preserve all fields)
    print(f"Loading instances from {instances_csv}...")
    try:
        with open(instances_csv, "r") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
    except Exception as e:
        print(f"Error: Failed to load instances from CSV: {e}")
        return 1

    if not rows:
        print("Warning: No instances found in CSV")
        return 0

    print(f"Loaded {len(rows)} instances")
    print(f"Checking for valid execution environments...")
    print()

    # Filter instances with valid execution environments
    valid_rows = []
    for row in rows:
        owner = row["owner"]
        repo = row["repo"]
        commit_hash = row["commit_hash"]
        short_hash = commit_hash[:8]

        if has_valid_execution_environment(owner, repo, commit_hash, instance_images_dir):
            valid_rows.append(row)
            print(f"  ✓ {owner}/{repo}/{short_hash}")
        else:
            print(f"  ✗ {owner}/{repo}/{short_hash} - no valid execution environment")

    print()
    print(f"Found {len(valid_rows)} instances with valid execution environments")
    print(f"Writing to {output_csv}...")

    # Write filtered instances to output CSV
    try:
        write_instances_csv(valid_rows, fieldnames, output_csv)
        print(f"Successfully wrote {len(valid_rows)} instances to {output_csv}")
    except Exception as e:
        print(f"Error: Failed to write output CSV: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
