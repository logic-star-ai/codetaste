"""Utility functions for metadata operations and path management."""

import json
import logging
import os
import secrets
import shutil
from datetime import datetime
from pathlib import Path
import subprocess
from typing import Optional

from refactoring_benchmark.inference.models import InferenceMetadata
from refactoring_benchmark.utils.models import InstanceRow
from podman.domain.containers import Container as PodmanContainer

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
        finish_reason: Reason for inference ending (e.g., "timeout")
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

def output_container_logs(container: PodmanContainer, output_path: Path, instance_logger: logging.Logger) -> None:
    """Helper to output container logs to file and logger."""
    raw_logs = container.logs(stream=False, follow=False)
    raw_logs = b"".join(raw_logs) if not isinstance(raw_logs, bytes) else raw_logs
    stdout = raw_logs.decode("utf-8", errors="replace")
    instance_logger.error(stdout)
    output_path.write_text(stdout, encoding="utf-8")

def cleanup_temp_dir(temp_description_dir: Path, instance_logger: logging.Logger) -> None:
    """Helper to cleanup temporary description directory."""
    if temp_description_dir and temp_description_dir.exists():
        try:
            shutil.rmtree(temp_description_dir)
        except Exception as e:
            try:
                subprocess.run(["podman", "unshare", "rm", "-rf", str(temp_description_dir)], check=False)
            except Exception as e2:
                instance_logger.error(f"Failed to remove temporary description directory: {e}, {e2}")

def prepare_temp_description(instance: InstanceRow, description_type: str, instance_logger: logging.Logger) -> Path:
    project_root = Path(__file__).parent.parent.parent
    source_dir = project_root / instance.asset_dir("descriptions")

    type_to_file = {
        "standard": "description.md",
        "minimal": "minimal_description.md",
        "nano": "nano_description.md",
        "open": "open_description.md",
        "abstract": "abstract_description.md",
    }

    source_filename = type_to_file.get(description_type)
    if not source_filename:
        raise ValueError(f"Unknown description_type: {description_type}. Valid types: {list(type_to_file.keys())}")

    source_file = source_dir / source_filename
    if not source_file.exists():
        raise FileNotFoundError(
            f"Description file not found for type '{description_type}': {source_file}. "
            f"Ensure the file exists in {source_dir}"
        )

    # Create temporary directory (don't use tempfile due to sticky bit issues)
    temp_dir = Path(f"./.tmp_descriptions/{instance.id}-{secrets.token_hex(8)}")
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Copy content as description.md (agents always read description.md)
    target_file = temp_dir / "description.md"
    content = source_file.read_text(encoding="utf-8")
    target_file.write_text(content, encoding="utf-8")

    # Set permissive permissions for container access
    os.chmod(temp_dir, 0o777)
    os.chmod(target_file, 0o777)

    instance_logger.debug(f"Prepared description: {source_filename} -> description.md")
    return temp_dir