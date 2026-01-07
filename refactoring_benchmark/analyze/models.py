"""Data models for analysis results."""

from typing import Dict
from pydantic import BaseModel, Field

from refactoring_benchmark.evaluation.models import RuleMetrics
from refactoring_benchmark.analyze.validation import ValidityStatus


class AgentIFRData(BaseModel):
    """IFR metrics and validity status for a single agent on a single instance."""

    positive_ifr: float = Field(ge=0, le=100, description="Positive IFR percentage")
    negative_ifr: float = Field(ge=0, le=100, description="Negative IFR percentage")
    total_ifr: float = Field(ge=0, le=100, description="Total IFR percentage")
    validity_status: ValidityStatus = Field(description="Test validity status")

    @classmethod
    def from_rule_metrics(cls, metrics: RuleMetrics, validity_status: ValidityStatus) -> "AgentIFRData":
        """Create AgentIFRData from RuleMetrics, converting to percentages."""
        return cls(
            positive_ifr=metrics.positive_ifr * 100,
            negative_ifr=metrics.negative_ifr * 100,
            total_ifr=metrics.ifr * 100,
            validity_status=validity_status,
        )


class InstanceData(BaseModel):
    """Data for all agents on a single instance."""

    instance_key: str = Field(description="Instance identifier: owner/repo/hash[:8]")
    agents: Dict[str, AgentIFRData] = Field(
        default_factory=dict, description="Agent ID to IFR data mapping"
    )


class AnalysisData(BaseModel):
    """Complete analysis data for all instances and agents."""

    instances: Dict[str, InstanceData] = Field(
        default_factory=dict, description="Instance key to instance data mapping"
    )

    def get_instance_keys_sorted(self) -> list[str]:
        """Get sorted list of instance keys."""
        return sorted(self.instances.keys())

    def get_agent_ids_sorted(self) -> list[str]:
        """Get sorted list of unique agent IDs across all instances."""
        agents = set()
        for instance_data in self.instances.values():
            agents.update(instance_data.agents.keys())
        return sorted(agents)

    def get_agent_data(self, instance_key: str, agent_id: str) -> AgentIFRData | None:
        """Get agent data for a specific instance and agent."""
        instance = self.instances.get(instance_key)
        if instance is None:
            return None
        return instance.agents.get(agent_id)
