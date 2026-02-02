#!/usr/bin/env python3
"""
Copy pseudo agent outputs to a new directory with updated description type.

This tool copies agent outputs (typically from output_pseudo_agents) to a new
location while updating the description_type field in both inference_metadata.json
and evaluation_result.json files.
"""

import argparse
import json
import shutil
from pathlib import Path
from typing import List

from refactoring_benchmark.evaluation.models import EvaluationResult
from refactoring_benchmark.inference.models import InferenceMetadata


def update_inference_metadata(metadata_path: Path, description_type: str) -> None:
    """
    Update the description_type field in an inference_metadata.json file.

    Args:
        metadata_path: Path to inference_metadata.json
        description_type: New description type value
    """
    with open(metadata_path, "r") as f:
        data = json.load(f)

    data["description_type"] = description_type

    # Validate with Pydantic model
    InferenceMetadata(**data)

    with open(metadata_path, "w") as f:
        json.dump(data, f, indent=2)


def update_evaluation_result(result_path: Path, description_type: str) -> None:
    """
    Update the description_type field in evaluation_result.json.

    Args:
        result_path: Path to evaluation_result.json
        description_type: New description type value
    """
    with open(result_path, "r") as f:
        data = json.load(f)

    # Update the nested inference_metadata.description_type field
    if "inference_metadata" in data and data["inference_metadata"] is not None:
        data["inference_metadata"]["description_type"] = description_type

    # Validate with Pydantic model
    EvaluationResult(**data)

    with open(result_path, "w") as f:
        json.dump(data, f, indent=4)


def copy_agent_output(
    source_path: Path,
    dest_path: Path,
    description_type: str,
    force: bool,
) -> None:
    """
    Copy a single agent output directory and update description type in all files.

    Args:
        source_path: Source agent output directory
        dest_path: Destination agent output directory
        description_type: Description type to set
        force: Whether to overwrite existing destination

    Raises:
        FileExistsError: If destination exists and force is False
    """
    if dest_path.exists():
        if not force:
            raise FileExistsError(f"Destination already exists: {dest_path}")
        shutil.rmtree(dest_path)

    # Copy entire directory tree
    shutil.copytree(source_path, dest_path)

    # Update inference_metadata.json
    inference_metadata_path = dest_path / "inference_metadata.json"
    if inference_metadata_path.exists():
        update_inference_metadata(inference_metadata_path, description_type)

    # Update evaluation_result.json
    evaluation_result_path = dest_path / "evaluation" / "evaluation_result.json"
    if evaluation_result_path.exists():
        update_evaluation_result(evaluation_result_path, description_type)


def discover_agents(source_dir: Path) -> List[str]:
    """
    Discover all agent IDs in the source directory.

    Args:
        source_dir: Source directory to scan

    Returns:
        List of agent IDs found (e.g., ["golden_agent", "null_agent"])
    """
    agent_ids = set()

    # Walk through directory structure: owner/repo/short_hash/agent_id/
    for agent_dir in source_dir.glob("*/*/*/*"):
        if agent_dir.is_dir() and (agent_dir / "inference_metadata.json").exists():
            agent_ids.add(agent_dir.name)

    return sorted(agent_ids)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy pseudo agent outputs with updated description type.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path.cwd() / "output_pseudo_agents",
        help="Source directory containing agent outputs",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Destination directory for copied agent outputs",
    )

    parser.add_argument(
        "--description-type",
        type=str,
        # required=True,
        # choices=["standard", "minimal", "nano", "open", "problem"],
        help="Description type to set in metadata files",
    )

    parser.add_argument(
        "--agent",
        action="append",
        dest="agents",
        help="Agent ID to copy (e.g., golden_agent, null_agent). Can be specified multiple times. If not specified, all agents are copied.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite destination if it already exists",
    )

    parser.add_argument(
        "--not-dry-run",
        action="store_true",
        help="Show what would be copied without actually copying",
    )

    args = parser.parse_args()

    # Resolve paths
    source_dir = args.source_dir.resolve()
    output_dir = args.output_dir.resolve()

    # Validate source directory
    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}")
        return 1

    # Discover available agents
    available_agents = discover_agents(source_dir)
    if not available_agents:
        print(f"Error: No agent outputs found in {source_dir}")
        return 1

    # Determine which agents to copy
    agents_to_copy = args.agents if args.agents else available_agents

    # Validate requested agents exist
    for agent_id in agents_to_copy:
        if agent_id not in available_agents:
            print(f"Error: Agent '{agent_id}' not found in source directory")
            print(f"Available agents: {', '.join(available_agents)}")
            return 1

    # Print summary
    print(f"Source directory: {source_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Description type: {args.description_type}")
    print(f"Agents to copy: {', '.join(agents_to_copy)}")
    print(f"Force overwrite: {args.force}")
    print(f"Dry run: {not args.not_dry_run}")
    print()

    # Find all agent output directories
    copy_tasks = []
    for agent_id in agents_to_copy:
        for agent_path in source_dir.glob(f"*/*/*/{agent_id}"):
            if not agent_path.is_dir():
                continue

            relative_path = agent_path.relative_to(source_dir)
            dest_path = output_dir / relative_path
            copy_tasks.append((agent_path, dest_path))

    if not copy_tasks:
        print("Warning: No agent outputs found to copy")
        return 0

    print(f"Found {len(copy_tasks)} agent output(s) to copy")
    print()

    # Execute copies
    success_count = 0
    error_count = 0

    for source_path, dest_path in copy_tasks:
        relative_display = dest_path.relative_to(output_dir)

        try:
            if not args.not_dry_run:
                print(f"  [DRY RUN] Would copy: {relative_display}")
                success_count += 1
            else:
                copy_agent_output(source_path, dest_path, args.description_type, args.force)
                print(f"  ✓ Copied: {relative_display}")
                success_count += 1

        except FileExistsError:
            print(f"  ✗ Skipped (exists): {relative_display}")
            print(f"    Use --force to overwrite")
            error_count += 1

        except Exception as e:
            print(f"  ✗ Error copying {relative_display}: {e}")
            error_count += 1

    print()
    print(f"Summary: {success_count} succeeded, {error_count} failed")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    exit(main())
