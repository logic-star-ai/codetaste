"""Compute statistics on IFR metrics across agents and instances."""

from typing import Dict, Literal
import statistics

from pydantic import BaseModel, Field

from refactoring_benchmark.analyze.models import AnalysisData, AgentIFRData
from refactoring_benchmark.analyze.validation import ValidityStatus


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


class CombinationStatistics(BaseModel):
    """Statistics for all agents under one filtering combination."""

    combination_id: int = Field(ge=1, le=6, description="Combination number (1-6)")
    ifr_condition: Literal["all", "ifr_gt_0"] = Field(description="IFR filtering condition")
    validity_condition: Literal["all", "valid", "invalid"] = Field(
        description="Test validity filtering condition"
    )
    agents: Dict[str, AgentStatistics] = Field(description="Statistics per agent")


class AllStatistics(BaseModel):
    """Complete statistics for all 6 combinations."""

    combinations: Dict[int, CombinationStatistics] = Field(
        description="Statistics for each combination (1-6)"
    )


def _compute_statistics(values: list[float]) -> MetricStatistics:
    """Compute mean and median for a list of values."""
    if not values:
        return MetricStatistics(mean=0.0, median=0.0, count=0)

    return MetricStatistics(
        mean=statistics.mean(values), median=statistics.median(values), count=len(values)
    )


def _filter_agent_data(
    data: AnalysisData,
    agent_id: str,
    ifr_condition: Literal["all", "ifr_gt_0"],
    validity_condition: Literal["all", "valid", "invalid"],
) -> list[AgentIFRData]:
    """
    Filter agent data based on IFR and validity conditions.

    Args:
        data: Analysis data containing all instances
        agent_id: Agent to filter for
        ifr_condition: Filter by IFR value (all or > 0)
        validity_condition: Filter by validity status (all, valid, or invalid)

    Returns:
        List of AgentIFRData that match the filtering conditions
    """
    filtered = []

    for instance_data in data.instances.values():
        agent_data = instance_data.agents.get(agent_id)
        if agent_data is None:
            continue

        # Apply IFR condition
        if ifr_condition == "ifr_gt_0" and agent_data.total_ifr <= 0:
            continue

        # Apply validity condition
        if validity_condition == "valid" and agent_data.validity_status != ValidityStatus.VALID:
            continue
        elif (
            validity_condition == "invalid"
            and agent_data.validity_status == ValidityStatus.VALID
        ):
            continue

        filtered.append(agent_data)

    return filtered


def compute_combination_statistics(
    data: AnalysisData,
    combination_id: int,
    ifr_condition: Literal["all", "ifr_gt_0"],
    validity_condition: Literal["all", "valid", "invalid"],
) -> CombinationStatistics:
    """
    Compute statistics for all agents under specific filtering conditions.

    Args:
        data: Analysis data to compute statistics from
        combination_id: Combination number (1-6) for identification
        ifr_condition: IFR filtering condition
        validity_condition: Test validity filtering condition

    Returns:
        CombinationStatistics containing per-agent statistics
    """
    agents = data.get_agent_ids_sorted()
    agent_stats = {}

    for agent_id in agents:
        # Get filtered data for this agent
        filtered_data = _filter_agent_data(data, agent_id, ifr_condition, validity_condition)

        if not filtered_data:
            # No data for this agent under these conditions
            agent_stats[agent_id] = AgentStatistics(
                agent_id=agent_id,
                total_ifr=MetricStatistics(mean=0.0, median=0.0, count=0),
                positive_ifr=MetricStatistics(mean=0.0, median=0.0, count=0),
                negative_ifr=MetricStatistics(mean=0.0, median=0.0, count=0),
            )
            continue

        # Extract metric values
        total_ifr_values = [d.total_ifr for d in filtered_data]
        positive_ifr_values = [d.positive_ifr for d in filtered_data]
        negative_ifr_values = [d.negative_ifr for d in filtered_data]

        # Compute statistics
        agent_stats[agent_id] = AgentStatistics(
            agent_id=agent_id,
            total_ifr=_compute_statistics(total_ifr_values),
            positive_ifr=_compute_statistics(positive_ifr_values),
            negative_ifr=_compute_statistics(negative_ifr_values),
        )

    return CombinationStatistics(
        combination_id=combination_id,
        ifr_condition=ifr_condition,
        validity_condition=validity_condition,
        agents=agent_stats,
    )


def compute_all_agent_statistics(data: AnalysisData) -> AllStatistics:
    """
    Compute statistics for all 6 combinations of filtering conditions.

    The 6 combinations are:
    1. All instances + All validity statuses
    2. All instances + Valid tests only
    3. All instances + Invalid tests only
    4. IFR > 0 instances + All validity statuses
    5. IFR > 0 instances + Valid tests only
    6. IFR > 0 instances + Invalid tests only

    Args:
        data: Analysis data to compute statistics from

    Returns:
        AllStatistics containing results for all 6 combinations
    """
    combinations = {}

    # Define the 6 combinations
    combination_configs = [
        (1, "all", "all"),
        (2, "all", "valid"),
        (3, "all", "invalid"),
        (4, "ifr_gt_0", "all"),
        (5, "ifr_gt_0", "valid"),
        (6, "ifr_gt_0", "invalid"),
    ]

    for combo_id, ifr_cond, validity_cond in combination_configs:
        combinations[combo_id] = compute_combination_statistics(
            data, combo_id, ifr_cond, validity_cond
        )

    return AllStatistics(combinations=combinations)
