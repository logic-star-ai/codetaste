"""Pydantic models for inference configuration and validation."""

from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator


class AgentInfo(BaseModel):
    """Agent information from agent_config.json."""

    name: str
    version: Optional[str] = None
    provider: str
    additional: Optional[Dict[str, Any]] = None


class ModelInfo(BaseModel):
    """Model information from agent_config.json."""

    name: str
    provider: str
    additional: Optional[Dict[str, Any]] = None


class AgentConfig(BaseModel):
    """Agent configuration loaded from agent_config.json."""

    id: str
    agent: AgentInfo
    model: ModelInfo


class InferenceConfig(BaseModel):
    """Runtime configuration for inference execution."""

    agent_dir: Path
    output_dir: Path
    instances_csv: Path
    nr_workers: int = Field(gt=0)
    timeout: int = Field(gt=0)
    instances_limit: int = Field(gt=0)
    force: bool
    agent_config: AgentConfig
    sanitized_agent_id: str

    class Config:
        arbitrary_types_allowed = True


class InferenceMetadata(BaseModel):
    """Metadata for inference results (created by agent or as fallback)."""

    cost_usd: float = Field(alias="cost_usd", default=-1.0)
    finish_reason: str
    finish_time: Optional[str] = None
    additional: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True
        extra = "allow"
