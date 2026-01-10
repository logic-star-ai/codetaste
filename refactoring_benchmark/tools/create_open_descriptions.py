#!/usr/bin/env python3
"""
Create open_description.md files for all instances.

For the 'open' description type, agents receive a simple open-ended prompt
without specific instructions about what to refactor.
"""

import csv
from pathlib import Path

# The open prompt text
OPEN_DESCRIPTION = "Autonomously identify and execute improvements to the **entire** codebase, without user intervention. Refactor the codebase. Improve structure, architecture, code quality and/or logic flow. Perform modifications on the actual codebase; do NOT output analysis, plan, roadmap or similar files."


def create_open_descriptions(instances_csv: Path, descriptions_dir: Path) -> None:
    """
    Create open_description.md files for all instances.

    Args:
        instances_csv: Path to instances.csv
        descriptions_dir: Path to assets/descriptions directory
    """
    success_count = 0
    error_count = 0

    with open(instances_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            owner = row["owner"]
            repo = row["repo"]
            commit_hash = row["commit_hash"]
            short_hash = commit_hash[:8]

            # Target directory
            target_dir = descriptions_dir / owner / repo / short_hash

            if not target_dir.exists():
                print(f"Warning: Directory does not exist: {target_dir}")
                error_count += 1
                continue

            # Create open_description.md
            open_desc_path = target_dir / "open_description.md"
            try:
                open_desc_path.write_text(OPEN_DESCRIPTION, encoding="utf-8")
                print(f"✓ Created: {open_desc_path}")
                success_count += 1
            except Exception as e:
                print(f"✗ Error creating {open_desc_path}: {e}")
                error_count += 1

    print(f"\nSummary:")
    print(f"  Success: {success_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total: {success_count + error_count}")


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent.parent
    instances_csv = project_root / "instances.csv"
    descriptions_dir = project_root / "assets" / "descriptions"

    if not instances_csv.exists():
        print(f"Error: instances.csv not found at {instances_csv}")
        return 1

    if not descriptions_dir.exists():
        print(f"Error: descriptions directory not found at {descriptions_dir}")
        return 1

    print("Creating open_description.md files...")
    print(f"  Instances CSV: {instances_csv}")
    print(f"  Descriptions dir: {descriptions_dir}")
    print()

    create_open_descriptions(instances_csv, descriptions_dir)
    return 0


if __name__ == "__main__":
    exit(main())
