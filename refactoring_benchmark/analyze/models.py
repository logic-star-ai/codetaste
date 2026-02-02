"""Data models for description-type based analysis."""

import math
import statistics
from typing import Dict, Literal

from pydantic import BaseModel, Field
from scipy import stats


class MetricPoint(BaseModel):
    """Single metric value for one instance."""

    instance_key: str = Field(description="Instance identifier (owner/repo/hash)")
    value: float  # = Field(ge=0, le=1, description="Metric value in [0, 1] range")


class AgentDescriptionData(BaseModel):
    """All metric values for one (agent_id, description_type) combination."""

    agent_id: str = Field(description="Agent identifier")
    description_type: str = Field(description="Description type (standard, minimal, nano, open)")
    metric_values: list[MetricPoint] = Field(default_factory=list, description="One value per instance")

    @property
    def count(self) -> int:
        """Number of data points."""
        return len(self.metric_values)

    @property
    def mean(self) -> float:
        """Mean of metric values."""
        if not self.metric_values:
            return 0.0
        return statistics.mean([p.value for p in self.metric_values])

    @property
    def standard_error(self) -> float:
        """Standard error of the mean: sigma / sqrt(n)."""
        if self.count <= 1:
            return 0.0
        return self.std / math.sqrt(self.count)

    def confidence_interval(self, confidence: float = 0.95) -> tuple[float, float]:
        """Calculate confidence interval for the mean using a T-distribution."""
        n = self.count
        if n <= 1:
            m = self.mean
            return (m, m)

        m = self.mean
        se = self.standard_error

        # Use t-distribution for small samples, which approaches Z as n grows
        h = se * stats.t.ppf((1 + confidence) / 2.0, n - 1)
        return m - h, m + h

    @property
    def median(self) -> float:
        """Median of metric values."""
        if not self.metric_values:
            return 0.0
        return statistics.median([p.value for p in self.metric_values])

    @property
    def std(self) -> float:
        """Standard deviation of metric values."""
        if len(self.metric_values) <= 1:
            return 0.0
        return statistics.stdev([p.value for p in self.metric_values])

    @property
    def min(self) -> float:
        """Minimum metric value."""
        if not self.metric_values:
            return 0.0
        return min(p.value for p in self.metric_values)

    @property
    def max(self) -> float:
        """Maximum metric value."""
        if not self.metric_values:
            return 0.0
        return max(p.value for p in self.metric_values)


class AnalysisData(BaseModel):
    """Complete analysis data grouped by (agent_id, description_type)."""

    # Key: (agent_id, description_type)
    data: Dict[tuple[str, str], AgentDescriptionData] = Field(
        default_factory=dict, description="Grouped data by agent and description type"
    )

    def add_metric_point(self, agent_id: str, description_type: str, instance_key: str, value: float) -> None:
        """Add a metric point to the analysis data.

        Args:
            agent_id: Agent identifier
            description_type: Description type
            instance_key: Instance identifier
            value: Metric value in [0, 1] range
        """
        key = (agent_id, description_type)
        if key not in self.data:
            self.data[key] = AgentDescriptionData(agent_id=agent_id, description_type=description_type)
        self.data[key].metric_values.append(MetricPoint(instance_key=instance_key, value=value))

    def get_agent_ids(self) -> list[str]:
        """Get sorted list of unique agent IDs with custom ordering."""
        agent_order = {
            "codex-v0.77.0-gpt-5.2": 0,
            "codex-v0.77.0-gpt-5.1-codex-mini": 1,
            "claude-code-v2.0.76-sonnet45": 2,
            "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct": 3,
            "golden_agent": 4,
            "null_agent": 5,
        }
        agents = set(k[0] for k in self.data.keys())
        return sorted(agents, key=lambda x: agent_order.get(x, 999))

    def get_description_types(self) -> list[str]:
        """Get sorted list of unique description types."""
        d = {"open": 0, "abstract": 10, "problem": 20, "nano": 30, "standard": 40}
        d_suffix = {"": 0, "plan": 1, "multiplan": 2}
        def sort_description_type(desc_type: str) -> tuple[int, int]:
            parts = desc_type.split("_")
            base = parts[0]
            suffix = parts[1] if len(parts) > 1 else ""
            return d.get(base, 100) + d_suffix.get(suffix, 5)
            
        return sorted(set(k[1] for k in self.data.keys()), key=sort_description_type)

    def get_data(self, agent_id: str, description_type: str) -> AgentDescriptionData | None:
        """Get data for a specific (agent_id, description_type) combination.

        Args:
            agent_id: Agent identifier
            description_type: Description type

        Returns:
            AgentDescriptionData if exists, None otherwise
        """
        return self.data.get((agent_id, description_type))

    def filter_agents(self, agent_ids: list[str]) -> "AnalysisData":
        """Create a new AnalysisData containing only specified agents.

        Args:
            agent_ids: List of agent IDs to keep

        Returns:
            New AnalysisData with filtered agents
        """
        filtered_data = AnalysisData()
        for (agent_id, description_type), agent_data in self.data.items():
            if agent_id in agent_ids:
                filtered_data.data[(agent_id, description_type)] = agent_data
        return filtered_data

    def filter_description_types(self, description_types: list[str]) -> "AnalysisData":
        """Create a new AnalysisData containing only specified description types.

        Args:
            description_types: List of description types to keep

        Returns:
            New AnalysisData with filtered description types
        """
        filtered_data = AnalysisData()
        for (agent_id, description_type), agent_data in self.data.items():
            if description_type in description_types:
                filtered_data.data[(agent_id, description_type)] = agent_data
        return filtered_data


AggregationType = Literal["mean", "median"]
