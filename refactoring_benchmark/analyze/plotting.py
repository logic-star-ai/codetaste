"""Generate plots comparing agents across description types."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from refactoring_benchmark.analyze.models import AnalysisData, AggregationType
from refactoring_benchmark.analyze.config import PlotConfig, PlotType


def create_plot(
    data: AnalysisData,
    metric_name: str,
    plot_type: PlotType = "line",
    aggregation: AggregationType = "mean",
    config: PlotConfig = PlotConfig(),
) -> plt.Figure:
    """Create a plot comparing agents across description types.

    Args:
        data: Analysis data containing metric values grouped by agent and description type
        metric_name: Name of the metric being plotted (for axis labels)
        plot_type: Type of plot ("line", "bar", "scatter")
        aggregation: How to aggregate values ("mean" or "median")
        config: Plot configuration settings

    Returns:
        Matplotlib figure object
    """
    agents = data.get_agent_ids()
    description_types = data.get_description_types()

    if not agents or not description_types:
        raise ValueError("No data to plot")

    # Create figure
    fig, ax = plt.subplots(figsize=(config.width, config.height))

    # Prepare colors for agents
    colors = plt.cm.tab10(np.linspace(0, 1, len(agents)))

    if plot_type == "line":
        _plot_line(ax, data, agents, description_types, colors, aggregation, config)
    elif plot_type == "bar":
        _plot_bar(ax, data, agents, description_types, colors, aggregation, config)
    elif plot_type == "scatter":
        _plot_scatter(ax, data, agents, description_types, colors, aggregation, config)
    else:
        raise ValueError(f"Unknown plot type: {plot_type}")

    # Configure axes
    ax.set_xlabel("Description Type", fontsize=config.xlabel_fontsize)
    ax.set_ylabel(f"{metric_name.upper()} ({aggregation})", fontsize=config.ylabel_fontsize)
    ax.set_title(
        f"{metric_name.upper()} by Description Type ({aggregation})",
        fontsize=config.title_fontsize,
        fontweight="bold",
    )
    ax.set_ylim(config.ylim_min, config.ylim_max)
    ax.legend(loc="best", fontsize=config.legend_fontsize)
    ax.grid(axis="y", alpha=config.grid_alpha, linestyle=config.grid_linestyle)

    plt.tight_layout()
    return fig


def _plot_line(
    ax: plt.Axes,
    data: AnalysisData,
    agents: list[str],
    description_types: list[str],
    colors: np.ndarray,
    aggregation: AggregationType,
    config: PlotConfig,
) -> None:
    """Plot line chart with error bars."""
    x = np.arange(len(description_types))

    for i, agent_id in enumerate(agents):
        values = []
        errors = []

        for desc_type in description_types:
            agent_desc_data = data.get_data(agent_id, desc_type)
            if agent_desc_data and agent_desc_data.count > 0:
                if aggregation == "mean":
                    values.append(agent_desc_data.mean)
                    errors.append(agent_desc_data.std / np.sqrt(agent_desc_data.count) if config.show_error_bars else 0.0)
                else:  # median
                    values.append(agent_desc_data.median)
                    errors.append(0.0)
            else:
                # Use np.nan for missing data (matplotlib handles this gracefully)
                values.append(np.nan)
                errors.append(np.nan)

        # Plot line
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

        # Plot error bars
        if config.show_error_bars:
            ax.errorbar(
                x,
                values,
                yerr=errors,
                fmt="none",
                ecolor=colors[i],
                capsize=config.error_bar_capsize,
                alpha=config.error_bar_alpha,
            )

    ax.set_xticks(x)
    ax.set_xticklabels(description_types, fontsize=config.tick_fontsize)


def _plot_bar(
    ax: plt.Axes,
    data: AnalysisData,
    agents: list[str],
    description_types: list[str],
    colors: np.ndarray,
    aggregation: AggregationType,
    config: PlotConfig,
) -> None:
    """Plot bar chart with error bars."""
    x = np.arange(len(description_types))
    width = config.bar_width / len(agents)

    for i, agent_id in enumerate(agents):
        values = []
        errors = []

        for desc_type in description_types:
            agent_desc_data = data.get_data(agent_id, desc_type)
            if agent_desc_data and agent_desc_data.count > 0:
                if aggregation == "mean":
                    values.append(agent_desc_data.mean)
                    errors.append(agent_desc_data.std / np.sqrt(agent_desc_data.count) if config.show_error_bars else 0.0)
                else:  # median
                    values.append(agent_desc_data.median)
                    errors.append(0.0)
            else:
                values.append(0.0)
                errors.append(0.0)

        # Plot bars
        ax.bar(
            x + i * width,
            values,
            width,
            label=agent_id,
            color=colors[i],
            alpha=config.bar_alpha,
            yerr=errors if config.show_error_bars else None,
            capsize=config.error_bar_capsize,
        )

    ax.set_xticks(x + width * (len(agents) - 1) / 2)
    ax.set_xticklabels(description_types, fontsize=config.tick_fontsize)


def _plot_scatter(
    ax: plt.Axes,
    data: AnalysisData,
    agents: list[str],
    description_types: list[str],
    colors: np.ndarray,
    aggregation: AggregationType,
    config: PlotConfig,
) -> None:
    """Plot scatter chart with error bars."""
    x = np.arange(len(description_types))

    for i, agent_id in enumerate(agents):
        values = []
        errors = []

        for desc_type in description_types:
            agent_desc_data = data.get_data(agent_id, desc_type)
            if agent_desc_data and agent_desc_data.count > 0:
                if aggregation == "mean":
                    values.append(agent_desc_data.mean)
                    errors.append(agent_desc_data.std / np.sqrt(agent_desc_data.count) if config.show_error_bars else 0.0)
                else:  # median
                    values.append(agent_desc_data.median)
                    errors.append(0.0)
            else:
                # Use np.nan for missing data (matplotlib handles this gracefully)
                values.append(np.nan)
                errors.append(np.nan)

        # Plot scatter points
        ax.scatter(
            x,
            values,
            label=agent_id,
            color=colors[i],
            s=config.marker_size**2,
            marker=config.marker_style,
            alpha=config.alpha,
        )

        # Plot error bars
        if config.show_error_bars:
            ax.errorbar(
                x,
                values,
                yerr=errors,
                fmt="none",
                ecolor=colors[i],
                capsize=config.error_bar_capsize,
                alpha=config.error_bar_alpha,
            )

    ax.set_xticks(x)
    ax.set_xticklabels(description_types, fontsize=config.tick_fontsize)


def save_plot(fig: plt.Figure, output_path: Path, dpi: int = 300) -> None:
    """Save plot to file.

    Args:
        fig: Matplotlib figure to save
        output_path: Path to save the plot
        dpi: Resolution for saved plot
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
