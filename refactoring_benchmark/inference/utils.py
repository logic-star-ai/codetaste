"""Utility functions for metadata operations and path management."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from refactoring_benchmark.inference.models import InferenceMetadata
from refactoring_benchmark.utils.models import InstanceRow


def get_instance_output_dir(instance: InstanceRow, agent_id: str, output_dir: Path) -> Path:
    """
    Construct the output directory path for a given instance and agent.

    Path structure: output/<owner>/<repo>/<hash[:8]>/<agent_id>/

    Args:
        instance: Benchmark instance
        agent_id: Sanitized agent ID
        output_dir: Base output directory

    Returns:
        Path to instance-specific output directory
    """
    return output_dir / instance.owner / instance.repo / instance.short_hash / agent_id


def copy_agent_config(agent_dir: Path, output_dir: Path) -> None:
    """
    Copy agent_config.json from agent directory to output directory.

    Args:
        agent_dir: Source agent directory
        output_dir: Destination output directory
    """
    src = agent_dir / "agent_config.json"
    dst = output_dir / "agent_config.json"

    if not src.exists():
        raise FileNotFoundError(f"Agent config not found: {src}")

    shutil.copy2(src, dst)


def create_fallback_inference_metadata(
    output_dir: Path,
    finish_reason: str,
    cost_usd: float = -1.0,
    additional: Optional[dict] = None,
    description_type: Optional[str] = None,
) -> None:
    """
    Create a fallback inference_metadata.json file for crashed or incomplete runs.

    Args:
        output_dir: Output directory where metadata should be saved
        finish_reason: Reason for inference ending (e.g., "crashed", "unknown", "timeout")
        cost_usd: Cost in USD (default: -1.0 for unknown)
        additional: Optional additional metadata
        description_type: Optional description type to include in metadata
    """
    metadata = InferenceMetadata(
        cost_usd=cost_usd,
        finish_reason=finish_reason,
        finish_time=datetime.utcnow().isoformat() + "Z",
        additional=additional or {},
    )

    output_path = output_dir / "inference_metadata.json"
    metadata_dict = metadata.model_dump(by_alias=True)

    # Add description_type if provided
    if description_type is not None:
        metadata_dict["description_type"] = description_type

    with open(output_path, "w") as f:
        json.dump(metadata_dict, f, indent=2)


def output_exists(output_dir: Path) -> bool:
    """
    Check if inference output already exists for this instance.

    Args:
        output_dir: Output directory to check

    Returns:
        True if prediction.diff exists, False otherwise
    """
    prediction_path = output_dir / "prediction.diff"
    return prediction_path.exists() and prediction_path.stat().st_size > 3

