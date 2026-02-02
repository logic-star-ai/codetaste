"""Pydantic models for inference configuration and validation."""

from pathlib import Path
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field, model_validator


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
    reuse_successful_plan: bool
    agent_config: AgentConfig
    sanitized_agent_id: str
    env_vars: Dict[str, str] = Field(default_factory=dict)
    description_type: str = "standard"
    plan: bool = False
    multiplan: bool = False
    plan_timeout: int = Field(gt=0, default=1800)

    @model_validator(mode="after")
    def validate_plan_modes(self) -> "InferenceConfig":
        """Ensure plan and multiplan are mutually exclusive."""
        if self.plan and self.multiplan:
            raise ValueError("Cannot enable both --plan and --multiplan simultaneously")
        return self

    class Config:
        arbitrary_types_allowed = True


FinishReason = Literal["success", "timeout", "execution_error", "error", "unknown", "budget_exceeded", "error_planmode", "error_multiplan", "error_judge"]


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


class MultiplanMetadata(BaseModel):
    """Metadata for multiplan generation and judgment phase."""

    start_time: str
    finish_time: Optional[str] = None
    finish_reason: FinishReason
    plans_generated: int = 0
    selected_plan_index: Optional[int] = None
    judge_reasoning: Optional[str] = None
    judge_cost_usd: Optional[float] = None
    judge_latency_seconds: Optional[float] = None
    judge_input_tokens: Optional[int] = None
    judge_output_tokens: Optional[int] = None

    @staticmethod
    def load_from_json(json_path: Path) -> "MultiplanMetadata":
        """Load MultiplanMetadata from a JSON file."""
        import json

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return MultiplanMetadata.model_validate(data)

    def save_to_json(self, json_path: Path) -> None:
        """Save MultiplanMetadata to a JSON file."""
        import json

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(), f, indent=2)
