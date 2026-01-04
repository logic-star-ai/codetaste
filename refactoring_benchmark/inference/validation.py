"""Validation and sanitization utilities for agent configuration."""

import json
import re
from pathlib import Path
from typing import Union

from refactoring_benchmark.inference.models import AgentConfig


def sanitize_agent_id(agent_id: str) -> str:
    """
    Sanitize agent ID to make it safe for use as a directory name.

    Replaces invalid filesystem characters with underscores and ensures
    the ID is not empty or consisting only of dots/spaces.

    Args:
        agent_id: Raw agent ID from agent_config.json

    Returns:
        Sanitized agent ID safe for filesystem use

    Raises:
        ValueError: If agent_id is empty or invalid after sanitization
    """
    if not agent_id or not agent_id.strip():
        raise ValueError("Agent ID cannot be empty")

    # Replace invalid filesystem characters with underscores
    # Invalid characters: / \ : * ? " < > |
    sanitized = re.sub(r'[/\\:*?"<>|]', "_", agent_id)

    # Replace whitespace with underscores
    sanitized = re.sub(r"\s+", "_", sanitized)

    # Remove leading/trailing dots and spaces (Windows issues)
    sanitized = sanitized.strip(". ")

    # Ensure result is not empty
    if not sanitized:
        raise ValueError(f"Agent ID '{agent_id}' results in empty string after sanitization")

    return sanitized


def validate_agent_config(config_path: Path) -> AgentConfig:
    """
    Load and validate agent configuration from JSON file.

    Args:
        config_path: Path to agent_config.json

    Returns:
        Validated AgentConfig instance

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If JSON is invalid or required fields are missing
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Agent config not found: {config_path}")

    try:
        with open(config_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in agent config: {e}")

    try:
        config = AgentConfig(**data)
    except Exception as e:
        raise ValueError(f"Invalid agent config structure: {e}")

    return config


def validate_agent_dir(agent_dir: Path) -> None:
    """
    Validate that the agent directory contains required files.

    Args:
        agent_dir: Path to agent directory

    Raises:
        FileNotFoundError: If directory or required files don't exist
        ValueError: If directory structure is invalid
    """
    if not agent_dir.exists():
        raise FileNotFoundError(f"Agent directory not found: {agent_dir}")

    if not agent_dir.is_dir():
        raise ValueError(f"Agent path is not a directory: {agent_dir}")

    # Check for required files
    required_files = {
        "agent_config.json": agent_dir / "agent_config.json",
        "run_agent": agent_dir / "run_agent",
    }

    optional_files = {
        "setup_agent.sh": agent_dir / "setup_agent.sh",
    }

    missing = []
    for name, path in required_files.items():
        if not path.exists():
            missing.append(name)

    if missing:
        raise FileNotFoundError(f"Missing required files in agent directory: {', '.join(missing)}")

    run_agent = required_files["run_agent"]
    if not run_agent.is_file():
        raise ValueError(f"run_agent is not a file: {run_agent}")
