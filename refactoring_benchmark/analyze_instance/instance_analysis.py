"""Instance-based analysis for comparing agent performance across benchmark instances."""

from pathlib import Path
from typing import Sequence

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel, Field

from refactoring_benchmark.analyze.config import PlotConfig
from refactoring_benchmark.analyze.filters import ResultFilter
from refactoring_benchmark.analyze.metrics import get_metric_function
from refactoring_benchmark.evaluation.models import EvaluationResult


class InstanceMetricPoint(BaseModel):
    """Single metric value for one agent on one instance."""

    agent_id: str = Field(description="Agent identifier")
    value: float = Field(ge=0, le=1, description="Metric value in [0, 1] range")


class InstanceData(BaseModel):
    """All metric values for one instance across multiple agents."""

    instance_key: str = Field(description="Instance identifier (owner/repo/hash)")
    instance_display: str = Field(description="Short display name for the instance")
    agent_values: dict[str, InstanceMetricPoint] = Field(default_factory=dict, description="Metric values by agent_id")

    def add_agent_value(self, agent_id: str, value: float) -> None:
        """Add a metric value for an agent."""
        self.agent_values[agent_id] = InstanceMetricPoint(agent_id=agent_id, value=value)

    def get_agent_value(self, agent_id: str) -> float | None:
        """Get metric value for a specific agent."""
        point = self.agent_values.get(agent_id)
        return point.value if point else None


class InstanceAnalysisData(BaseModel):
    """Complete analysis data grouped by instance."""

    # Key: instance_key (owner/repo/hash)
    instances: dict[str, InstanceData] = Field(default_factory=dict, description="Data by instance")

    def add_metric_point(self, instance_key: str, instance_display: str, agent_id: str, value: float) -> None:
        """Add a metric point to the analysis data.

        Args:
            instance_key: Full instance identifier (owner/repo/hash)
            instance_display: Short display name for the instance
            agent_id: Agent identifier
            value: Metric value in [0, 1] range
        """
        if instance_key not in self.instances:
            self.instances[instance_key] = InstanceData(instance_key=instance_key, instance_display=instance_display)
        self.instances[instance_key].add_agent_value(agent_id, value)

    def get_instance_keys(self) -> list[str]:
        """Get sorted list of instance keys."""
        return sorted(self.instances.keys())

    def get_agent_ids(self) -> list[str]:
        """Get sorted list of unique agent IDs across all instances."""
        agent_ids = set()
        for instance_data in self.instances.values():
            agent_ids.update(instance_data.agent_values.keys())
        return sorted(agent_ids)

    def filter_agents(self, agent_ids: list[str]) -> "InstanceAnalysisData":
        """Create a new InstanceAnalysisData containing only specified agents.

        Args:
            agent_ids: List of agent IDs to keep

        Returns:
            New InstanceAnalysisData with filtered agents
        """
        filtered_data = InstanceAnalysisData()
        for instance_key, instance_data in self.instances.items():
            for agent_id in agent_ids:
                if agent_id in instance_data.agent_values:
                    filtered_data.add_metric_point(
                        instance_key,
                        instance_data.instance_display,
                        agent_id,
                        instance_data.agent_values[agent_id].value,
                    )
        return filtered_data

    def filter_instances(self, instance_keys: list[str]) -> "InstanceAnalysisData":
        """Create a new InstanceAnalysisData containing only specified instances.

        Args:
            instance_keys: List of instance keys to keep

        Returns:
            New InstanceAnalysisData with filtered instances
        """
        filtered_data = InstanceAnalysisData()
        for instance_key in instance_keys:
            if instance_key in self.instances:
                instance_data = self.instances[instance_key]
                for agent_id, point in instance_data.agent_values.items():
                    filtered_data.add_metric_point(instance_key, instance_data.instance_display, agent_id, point.value)
        return filtered_data


def organize_instance_data(
    results: list[EvaluationResult],
    metric_name: str,
    filters: Sequence[ResultFilter] | None = None,
) -> InstanceAnalysisData:
    """Organize evaluation results by instance with the given metric.

    Args:
        results: List of evaluation results to organize
        metric_name: Name of the metric to extract (e.g., "ifr", "test_success")
        filters: Optional list of filter functions to apply (AND logic)

    Returns:
        InstanceAnalysisData containing organized metric values grouped by instance

    Example:
        >>> from refactoring_benchmark.analyze.filters import filter_successful_only
        >>> data = organize_instance_data(results, "ifr", filters=[filter_successful_only()])
    """
    # Get metric function
    metric_fn = get_metric_function(metric_name)
    analysis_data = InstanceAnalysisData()

    for result in results:
        # Apply filters if provided
        if filters:
            if not all(filter_fn(result) for filter_fn in filters):
                continue

        # Extract metric value
        metric_value = metric_fn(result)
        if metric_value is None:
            # Skip this result if metric cannot be computed
            continue

        # Create instance key and display name
        instance_key = (
            f"{result.instance_metadata.owner}/{result.instance_metadata.repo}/{result.instance_metadata.base_hash[:8]}"
        )
        instance_display = f"{result.instance_metadata.repo[:20]}/{result.instance_metadata.base_hash[:8]}"

        # Extract agent_id
        agent_id = result.agent_config.id

        # Add to analysis data
        analysis_data.add_metric_point(instance_key, instance_display, agent_id, metric_value)

    return analysis_data


def create_instance_plot(
    data: InstanceAnalysisData,
    metric_name: str,
    plot_type: str = "line",
    config: PlotConfig = PlotConfig(),
    max_instances: int | None = None,
) -> plt.Figure:
    """Create a plot comparing agents across instances.

    Args:
        data: Instance analysis data containing metric values
        metric_name: Name of the metric being plotted (for axis labels)
        plot_type: Type of plot ("line", "bar", "heatmap")
        config: Plot configuration settings
        max_instances: Maximum number of instances to display (defaults to all)

    Returns:
        Matplotlib figure object
    """
    instance_keys = data.get_instance_keys()
    agents = data.get_agent_ids()

    if not instance_keys or not agents:
        raise ValueError("No data to plot")

    # Limit number of instances if specified
    if max_instances and len(instance_keys) > max_instances:
        instance_keys = instance_keys[:max_instances]

    # Get display names for instances
    instance_displays = [data.instances[key].instance_display for key in instance_keys]

    if plot_type == "heatmap":
        return _plot_instance_heatmap(data, metric_name, instance_keys, instance_displays, agents, config)
    elif plot_type == "line":
        return _plot_instance_line(data, metric_name, instance_keys, instance_displays, agents, config)
    elif plot_type == "bar":
        return _plot_instance_bar(data, metric_name, instance_keys, instance_displays, agents, config)
    else:
        raise ValueError(f"Unknown plot type: {plot_type}")


def _plot_instance_heatmap(
    data: InstanceAnalysisData,
    metric_name: str,
    instance_keys: list[str],
    instance_displays: list[str],
    agents: list[str],
    config: PlotConfig,
) -> plt.Figure:
    """Create a heatmap showing metric values for each (instance, agent) pair."""

    # 1. Initialize matrix with NaNs instead of zeros
    matrix = np.full((len(agents), len(instance_keys)), np.nan)

    for i, agent_id in enumerate(agents):
        for j, instance_key in enumerate(instance_keys):
            instance_data = data.instances[instance_key]
            value = instance_data.get_agent_value(agent_id)
            # 2. Keep value as None/NaN if it's missing
            if value is not None:
                matrix[i, j] = value

    # Create figure with appropriate size
    fig_width = max(10, len(instance_keys) * 0.4)
    fig_height = max(6, len(agents) * 0.5)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # 3. Configure the colormap to show NaNs as black
    current_cmap = cm.get_cmap("RdYlGn").copy()
    current_cmap.set_bad(color="black")

    # 4. Use the modified colormap
    im = ax.imshow(matrix, cmap=current_cmap, aspect="auto", vmin=0, vmax=1)

    # Set ticks and labels
    ax.set_xticks(np.arange(len(instance_keys)))
    ax.set_yticks(np.arange(len(agents)))
    ax.set_xticklabels(instance_displays, rotation=45, ha="right", fontsize=config.tick_fontsize)
    ax.set_yticklabels(agents, fontsize=config.tick_fontsize)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(metric_name.upper(), fontsize=config.ylabel_fontsize)

    # Add title
    ax.set_title(
        f"{metric_name.upper()} by Instance and Agent",
        fontsize=config.title_fontsize,
        fontweight="bold",
        pad=20,
    )

    ax.set_xlabel("Instance", fontsize=config.xlabel_fontsize)
    ax.set_ylabel("Agent", fontsize=config.ylabel_fontsize)

    plt.tight_layout()
    return fig


def _plot_instance_line(
    data: InstanceAnalysisData,
    metric_name: str,
    instance_keys: list[str],
    instance_displays: list[str],
    agents: list[str],
    config: PlotConfig,
) -> plt.Figure:
    """Create a line plot comparing agents across instances."""
    # Create figure with appropriate width for many instances
    fig_width = max(config.width, len(instance_keys) * 0.5)
    fig, ax = plt.subplots(figsize=(fig_width, config.height))

    x = np.arange(len(instance_keys))
    colors = plt.cm.tab10(np.linspace(0, 1, len(agents)))

    for i, agent_id in enumerate(agents):
        values = []
        for instance_key in instance_keys:
            instance_data = data.instances[instance_key]
            value = instance_data.get_agent_value(agent_id)
            values.append(value if value is not None else np.nan)

        ax.plot(
            x,
            values,
            label=agent_id,
            color=colors[i],
            linewidth=config.line_width,
            marker=config.marker_style,
            markersize=config.marker_size,
            alpha=config.alpha,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(instance_displays, rotation=45, ha="right", fontsize=config.tick_fontsize)
    ax.set_xlabel("Instance", fontsize=config.xlabel_fontsize)
    ax.set_ylabel(metric_name.upper(), fontsize=config.ylabel_fontsize)
    ax.set_title(
        f"{metric_name.upper()} by Instance",
        fontsize=config.title_fontsize,
        fontweight="bold",
    )
    ax.set_ylim(config.ylim_min, config.ylim_max)
    ax.legend(loc="best", fontsize=config.legend_fontsize)
    ax.grid(axis="y", alpha=config.grid_alpha, linestyle=config.grid_linestyle)

    plt.tight_layout()
    return fig


def _plot_instance_bar(
    data: InstanceAnalysisData,
    metric_name: str,
    instance_keys: list[str],
    instance_displays: list[str],
    agents: list[str],
    config: PlotConfig,
) -> plt.Figure:
    """Create a bar plot comparing agents across instances."""
    # Create figure with appropriate width for many instances
    fig_width = max(config.width, len(instance_keys) * 0.8)
    fig, ax = plt.subplots(figsize=(fig_width, config.height))

    x = np.arange(len(instance_keys))
    width = config.bar_width / len(agents)
    colors = plt.cm.tab10(np.linspace(0, 1, len(agents)))

    for i, agent_id in enumerate(agents):
        values = []
        for instance_key in instance_keys:
            instance_data = data.instances[instance_key]
            value = instance_data.get_agent_value(agent_id)
            values.append(value if value is not None else 0.0)

        ax.bar(
            x + i * width,
            values,
            width,
            label=agent_id,
            color=colors[i],
            alpha=config.bar_alpha,
        )

    ax.set_xticks(x + width * (len(agents) - 1) / 2)
    ax.set_xticklabels(instance_displays, rotation=45, ha="right", fontsize=config.tick_fontsize)
    ax.set_xlabel("Instance", fontsize=config.xlabel_fontsize)
    ax.set_ylabel(metric_name.upper(), fontsize=config.ylabel_fontsize)
    ax.set_title(
        f"{metric_name.upper()} by Instance",
        fontsize=config.title_fontsize,
        fontweight="bold",
    )
    ax.set_ylim(config.ylim_min, config.ylim_max)
    ax.legend(loc="best", fontsize=config.legend_fontsize)
    ax.grid(axis="y", alpha=config.grid_alpha, linestyle=config.grid_linestyle)

    plt.tight_layout()
    return fig


def save_instance_plot(fig: plt.Figure, output_path: Path, dpi: int = 300) -> None:
    """Save plot to file.

    Args:
        fig: Matplotlib figure to save
        output_path: Path to save the plot
        dpi: Resolution for saved plot
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
