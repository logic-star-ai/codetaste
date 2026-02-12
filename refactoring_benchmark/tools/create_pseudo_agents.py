#!/usr/bin/env python3
"""
Create pseudo agent outputs for golden and null agents.

Golden agent: Copies the golden.diff from assets/diffs as the prediction
Null agent: Creates an empty prediction (single newline)

Both agents create proper output structure with agent_config.json and inference_metadata.json
"""

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from refactoring_benchmark.inference.models import (
    AgentConfig,
    AgentInfo,
    InferenceMetadata,
    ModelInfo,
)
from refactoring_benchmark.utils.common import load_instances_from_csv
from refactoring_benchmark.utils.models import InstanceRow

PSEUDO_AGENTS = {
    "golden": {
        "id": "golden_agent",
        "agent": {"name": "golden_agent", "version": "0.0.0", "provider": "golden", "additional": None},
        "model": {"name": "golden_model", "provider": "golden", "additional": None},
    },
    "null": {
        "id": "null_agent",
        "agent": {"name": "null_agent", "version": "0.0.0", "provider": "null", "additional": None},
        "model": {"name": "null_model", "provider": "null", "additional": None},
    },
}


def create_agent_output(
    instance: InstanceRow,
    agent_type: str,
    output_dir: Path,
    assets_base: Path,
) -> None:
    """
    Create pseudo agent output for a single instance.

    Args:
        instance: Instance to create output for
        agent_type: Type of agent ("golden" or "null")
        output_dir: Base output directory
        assets_base: Base directory for assets (for golden.diff)
    """
    # Get agent config
    agent_config_dict = PSEUDO_AGENTS[agent_type]
    agent_id = agent_config_dict["id"]

    # Create output directory: output_dir/owner/repo/short_hash/agent_id/
    instance_output_dir = output_dir / instance.owner / instance.repo / instance.short_hash / agent_id
    instance_output_dir.mkdir(parents=True, exist_ok=True)

    # Create agent_config.json
    agent_config = AgentConfig(
        id=agent_config_dict["id"],
        agent=AgentInfo(**agent_config_dict["agent"]),
        model=ModelInfo(**agent_config_dict["model"]),
    )
    agent_config_path = instance_output_dir / "agent_config.json"
    with open(agent_config_path, "w") as f:
        json.dump(agent_config.model_dump(), f, indent=2)

    # Create inference_metadata.json with current timestamp
    current_time = datetime.now(timezone.utc).isoformat(timespec="seconds")
    metadata = InferenceMetadata(
        cost_usd=0.0,
        finish_reason="success",
        start_time=current_time,
        finish_time=current_time,
        additional=None,
    )
    metadata_path = instance_output_dir / "inference_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata.model_dump(), f, indent=2)

    # Create prediction.diff
    prediction_path = instance_output_dir / "prediction.diff"

    if agent_type == "golden":
        # Copy from assets/diffs/owner/repo/short_hash/golden.diff
        golden_diff_path = assets_base / "diffs" / instance.owner / instance.repo / instance.short_hash / "golden.diff"

        if not golden_diff_path.exists():
            print(f"  Warning: Golden diff not found at {golden_diff_path}, creating empty prediction")
            prediction_path.write_text("\n")
        else:
            shutil.copy2(golden_diff_path, prediction_path)

    elif agent_type == "null":
        # Create empty diff (single newline)
        prediction_path.write_text("\n")

    print(f"  ✓ Created {agent_id} output for {instance.display_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Create pseudo agent outputs (golden_agent and null_agent) for benchmark instances.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path(__file__).parent.parent.parent / "instances.csv",
        help="Path to instances CSV file",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "outputs" / "pseudo_agents" / "direct",
        help="Base directory for pseudo agent outputs",
    )

    parser.add_argument(
        "--agent",
        action="append",
        choices=["golden", "null"],
        dest="agents",
        help="Agent type to create (can be specified multiple times, e.g., --agent golden --agent null)",
    )

    parser.add_argument(
        "--assets-base",
        type=Path,
        default=Path(__file__).parent.parent.parent / "assets",
        help="Base directory for assets (contains diffs/)",
    )

    args = parser.parse_args()

    # Validate agents specified
    if not args.agents:
        parser.error("At least one --agent must be specified (golden or null)")

    # Resolve paths
    instances_csv = args.instances_csv.resolve()
    output_dir = args.output_dir.resolve()
    assets_base = args.assets_base.resolve()

    # Validate instances CSV exists
    if not instances_csv.exists():
        print(f"Error: instances.csv not found at {instances_csv}")
        return 1

    # Load instances
    print(f"Loading instances from {instances_csv}...")
    try:
        instances = load_instances_from_csv(instances_csv)
    except Exception as e:
        print(f"Error: Failed to load instances from CSV: {e}")
        return 1

    if not instances:
        print("Warning: No instances found in CSV")
        return 0

    print(f"Loaded {len(instances)} instances")
    print(f"Creating pseudo agents: {', '.join(args.agents)}")
    print(f"Output directory: {output_dir}")
    print()

    # Create outputs
    for agent_type in args.agents:
        print(f"Creating {agent_type}_agent outputs...")
        for instance in instances:
            try:
                create_agent_output(instance, agent_type, output_dir, assets_base)
            except Exception as e:
                print(f"  ✗ Error creating {agent_type}_agent output for {instance.display_path}: {e}")
        print()

    print("Done!")
    return 0


if __name__ == "__main__":
    exit(main())
