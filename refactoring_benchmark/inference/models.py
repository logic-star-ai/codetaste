"""Pydantic models for inference configuration and validation."""

from pathlib import Path
from typing import Any, Dict, Literal, Optional

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
    force_unsuccessful: bool
    agent_config: AgentConfig
    sanitized_agent_id: str
    env_vars: Dict[str, str] = Field(default_factory=dict)
    description_type: str = "standard"

    class Config:
        arbitrary_types_allowed = True

FinishReason = Literal["success", "timeout", "execution_error", "unknown", "budget_exceeded"]

class InferenceMetadata(BaseModel):
    """Metadata for inference results (created by agent or as fallback)."""

    cost_usd: float = Field(alias="cost_usd", default=-1.0)
    finish_reason: FinishReason
    finish_time: Optional[str] = None
    start_time: Optional[str] = None
    additional: Optional[Dict[str, Any]] = None
    description_type: Optional[str] = None

    class Config:
        populate_by_name = True
        extra = "allow"


    def load_from_json(json_path: Path) -> "InferenceMetadata":
        """Load InferenceMetadata from a JSON file."""
        import json

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return InferenceMetadata.model_validate(data)
    
    def save_to_json(self, json_path: Path) -> None:
        """Save InferenceMetadata to a JSON file."""
        import json

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(by_alias=True), f, indent=2)