"""Utility functions for metadata operations and path management."""

import json
import logging
import secrets
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.inference.models import (
    ExecutionContext,
    InferenceConfig,
    InferenceMetadata,
)
from refactoring_benchmark.utils.models import InstanceRow

DEFAULT_PREFIX = """Perform the task described below in it's ENTIRETY. You operate completely AUTONOMOUSLY in a sandboxed environment. DO NOT ASK FOR CLARIFICATIONS. You must EDIT the codebase DIRECTLY to complete the task. DO NOT create reports, plans or similar files.\n"""

PLAN_PREFIX = """Conduct IN-DEPTH EXPLORATION and ANALYSIS of the codebase.
Refine the following task description into a CONCRETE and ACTIONABLE refactoring plan. Make ALL the design choices. DO NOT propose broad, multi-stage changes.
You operate completely AUTONOMOUSLY in this sandboxed environment. DO NOT ASK FOR CLARIFICATIONS.
The final plan must be in markdown format:
```
# Title
<Summary>
## Changes
...
## Why
...
```
You MUST PLACE the final plan in this file: '/output/refactoring_plan.md'.

Task:
"""

NUM_MULTIPLAN = 5

MULTIPLAN_PREFIX = f"""Conduct IN-DEPTH EXPLORATION and ANALYSIS of the codebase.
Generate {NUM_MULTIPLAN} DISTINCT and DIFFERENT refactoring plans for the following task. There can be partial overlap.
You operate completely AUTONOMOUSLY in this sandboxed environment. DO NOT ASK FOR CLARIFICATIONS.

For each approach, create a COMPLETE, CONCRETE and ACTIONABLE refactoring plan. Make ALL the design choices. DO NOT propose broad, multi-stage changes.
Each plan must be in markdown format:
```
# Title
<Summary>
## Changes
...
## Why
...
```

You MUST create EXACTLY {NUM_MULTIPLAN} plans and save them as:
{chr(10).join(f"- '/output/refactoring_plans/refactoring_plan{i}.md'" for i in range(NUM_MULTIPLAN))}

Task:
"""

DESCRIPTION_FILES = {
    "instructed": "description.md",
    "open": "open_description.md",
}
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_instance_output_dir(instance: InstanceRow, agent_id: str, output_dir: Path) -> Path:
    """
    Construct the output directory path for a given instance and agent.

    Path structure: outputs/<description_type>/<mode>/<owner>/<repo>/<hash[:8]>/<agent_id>/

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
    mode: Optional[str] = None,
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
        finish_time=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        additional=additional or {},
        description_type=description_type,
        mode=mode,
    )

    output_path = output_dir / "inference_metadata.json"
    metadata_dict = metadata.model_dump(by_alias=True)

    # Add description_type if provided
    if description_type is not None:
        metadata_dict["description_type"] = description_type
    if mode is not None:
        metadata_dict["mode"] = mode

    with open(output_path, "w") as f:
        json.dump(metadata_dict, f, indent=2)


def finalize_step_metadata(
    src: Path,
    dst: Path,
    description_type: str,
    mode: str,
    logger: Optional[logging.Logger] = None,
) -> None:
    """Rename step metadata and ensure description_type/mode are persisted."""
    if not src.exists():
        message = f"Missing metadata file: {src}"
        if logger:
            logger.error(message)
        raise FileNotFoundError(message)

    try:
        src.rename(dst)
        inference_metadata: InferenceMetadata = InferenceMetadata.load_from_json(dst)
        inference_metadata.description_type = description_type
        inference_metadata.mode = mode
        inference_metadata.save_to_json(dst)
        if logger:
            logger.info(f"Renamed {src.name} to {dst.name}")
    except Exception as e:
        message = f"Failed to rename {src.name} to {dst.name}: {e}"
        if logger:
            logger.error(message)
        raise RuntimeError(message) from e


def build_context(
    config: InferenceConfig,
    plan_path: Optional[Path] = None,
    plan_content: Optional[str] = None,
    mode: Optional[str] = None,
) -> ExecutionContext:
    """Build an ExecutionContext with consistent mode/description wiring."""
    if mode is None:
        if plan_content is not None:
            mode = "multiplan"
        elif plan_path is not None:
            mode = "plan"
        else:
            mode = config.mode

    return ExecutionContext(
        description_type=config.description_type,
        mode=mode,
        plan_path=plan_path,
        plan_content=plan_content,
    )


def output_exists(output_dir: Path) -> bool:
    """
    Check if inference output already exists for this instance.

    Args:
        output_dir: Output directory to check

    Returns:
        True if prediction.diff exists, False otherwise
    """
    prediction_path = output_dir / "prediction.diff"
    return prediction_path.exists()


def output_container_logs(container: PodmanContainer, output_path: Path, instance_logger: logging.Logger) -> None:
    """Helper to output container logs to file and logger."""
    raw_logs = container.logs(stream=False, follow=False)
    raw_logs = b"".join(raw_logs) if not isinstance(raw_logs, bytes) else raw_logs
    stdout = raw_logs.decode("utf-8", errors="replace")
    instance_logger.info(stdout)
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


def _load_template(instance: InstanceRow, description_type: str) -> str:
    """Internal helper to read a description template from disk."""
    filename = DESCRIPTION_FILES.get(description_type)
    if not filename:
        raise ValueError(f"Unknown type: {description_type}. Valid: {list(DESCRIPTION_FILES.keys())}")

    path = (PROJECT_ROOT / instance.asset_dir("descriptions") / filename).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")

    return path.read_text(encoding="utf-8")


def create_temporary_description_dir(instance: InstanceRow, content: str) -> Path:
    """Creates a temporary directory, writes description.md, and sets 0o777 permissions."""
    temp_dir = Path(f"./.tmp_descriptions/{instance.id}-{secrets.token_hex(8)}")
    temp_dir.mkdir(parents=True, exist_ok=True)

    target_file = temp_dir / "description.md"
    target_file.write_text(content, encoding="utf-8")

    for p in [temp_dir, target_file]:
        p.chmod(0o777)
    return temp_dir.resolve()


def prepare_temp_task_description(
    instance: InstanceRow, logger: logging.Logger, description_type: Optional[str] = None, content: Optional[str] = None
) -> Path:
    """Prepares a task description using either a template type OR direct content."""
    base_content = content or _load_template(instance, description_type)
    full_content = f"{DEFAULT_PREFIX}\n\n{base_content}"
    logger.debug(f"Prepared Task Description (Type: {description_type or 'Injected'})")
    return create_temporary_description_dir(instance, full_content)


def prepare_temp_plan_description(
    instance: InstanceRow, logger: logging.Logger, description_type: Optional[str] = None, content: Optional[str] = None
) -> Path:
    """Prepares a plan description using either a template type OR direct content."""
    base_content = content or _load_template(instance, description_type)
    full_content = f"{PLAN_PREFIX}\n\n{base_content}"
    logger.debug(f"Prepared Plan Description (Type: {description_type or 'Injected'})")
    return create_temporary_description_dir(instance, full_content)


def prepare_temp_multiplan_description(
    instance: InstanceRow, logger: logging.Logger, description_type: Optional[str] = None, content: Optional[str] = None
) -> Path:
    """Prepares a multiplan description using either a template type OR direct content."""
    base_content = content or _load_template(instance, description_type)
    full_content = f"{MULTIPLAN_PREFIX}\n\n{base_content}"
    logger.debug(f"Prepared Multiplan Description (Type: {description_type or 'Injected'})")
    return create_temporary_description_dir(instance, full_content)
