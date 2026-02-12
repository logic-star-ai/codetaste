"""Data models for analysis results."""

from typing import Dict, Literal

from pydantic import BaseModel, Field

from refactoring_benchmark.analyze.validation import ValidityStatus
from refactoring_benchmark.evaluation.models import RuleMetrics
from refactoring_benchmark.utils.models import ReducedInstanceRow


class AgentInstanceStats(BaseModel):
    """IFR metrics and validity status for a single agent on a single instance."""

    positive_ifr: float = Field(ge=0, le=100, description="Positive IFR percentage")
    negative_ifr: float = Field(ge=0, le=100, description="Negative IFR percentage")
    total_ifr: float = Field(ge=0, le=100, description="Total IFR percentage")
    validity_status: ValidityStatus = Field(description="Test validity status")

    # Optional precision metrics
    precision_added: float | None = Field(None, ge=0, le=100, description="Precision of additions percentage")
    precision_removed: float | None = Field(None, ge=0, le=100, description="Precision of deletions percentage")
    precision_overall: float | None = Field(None, ge=0, le=100, description="Overall precision percentage")

    cost_usd: float = Field(default=-1.0, description="Cost in USD, -1 if missing, 0 for pseudo agents")

    @classmethod
    def from_rule_metrics(cls, metrics: RuleMetrics, validity_status: ValidityStatus) -> "AgentInstanceStats":
        """Create AgentIFRData from RuleMetrics, converting to percentages."""
        return cls(
            positive_ifr=metrics.positive_ifr * 100,
            negative_ifr=metrics.negative_ifr * 100,
            total_ifr=metrics.ifr * 100,
            validity_status=validity_status,
        )


class InstanceData(BaseModel):
    """Data for all agents on a single instance."""

    instance: ReducedInstanceRow = Field(description="Full instance row data")
    agents: Dict[str, AgentInstanceStats] = Field(default_factory=dict, description="Agent ID to IFR data mapping")


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

    def get_agent_data(self, instance_key: str, agent_id: str) -> AgentInstanceStats | None:
        """Get agent data for a specific instance and agent."""
        instance = self.instances.get(instance_key)
        if instance is None:
            return None
        return instance.agents.get(agent_id)


##
class MetricStatistics(BaseModel):
    """Statistics for a single IFR metric."""

    mean: float = Field(description="Average value")
    median: float = Field(description="Median value")
    count: int = Field(ge=0, description="Number of instances included")


class AgentStatistics(BaseModel):
    """Complete statistics for one agent under specific filtering conditions."""

    agent_id: str = Field(description="Agent identifier")
    total_ifr: MetricStatistics = Field(description="Total IFR statistics")
    positive_ifr: MetricStatistics = Field(description="Positive IFR statistics")
    negative_ifr: MetricStatistics = Field(description="Negative IFR statistics")
    precision_added: MetricStatistics = Field(description="Precision of additions statistics")
    precision_removed: MetricStatistics = Field(description="Precision of deletions statistics")
    precision_overall: MetricStatistics = Field(description="Overall precision statistics")
    avg_cost_usd: MetricStatistics = Field(description="Average cost in USD statistics")


class CombinationStatistics(BaseModel):
    """Statistics for all agents under one filtering combination."""

    combination_id: int = Field(ge=1, le=6, description="Combination number (1-6)")
    ifr_condition: Literal["all", "ifr_gt_0"] = Field(description="IFR filtering condition")
    validity_condition: Literal["all", "valid", "invalid"] = Field(description="Test validity filtering condition")
    agents: Dict[str, AgentStatistics] = Field(description="Statistics per agent")


class AllStatistics(BaseModel):
    """Complete statistics for all 6 combinations."""

    combinations: Dict[int, CombinationStatistics] = Field(description="Statistics for each combination (1-6)")
