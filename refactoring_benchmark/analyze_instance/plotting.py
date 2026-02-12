"""Generate IFR plots by agent and instance."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from refactoring_benchmark.analyze.config import (
    IFR_PLOT_DEFINITIONS,
    IFRMetricType,
    IFRPlotConfig,
)
from refactoring_benchmark.analyze.validation import ValidityStatus
from refactoring_benchmark.analyze_instance.models import AnalysisData


def create_ifr_plot(
    data: AnalysisData, metric_key: IFRMetricType, title: str, config: IFRPlotConfig = IFRPlotConfig()
) -> plt.Figure:
    """
    Create a bar chart for a specific IFR metric.

    Args:
        data: Analysis data containing IFR metrics
        metric_key: Which IFR metric to plot
        title: Plot title
        config: Plot configuration settings

    Returns:
        Matplotlib figure object
    """
    instances = data.get_instance_keys_sorted()
    agents = data.get_agent_ids_sorted()

    # Calculate figure size
    fig_width = max(config.min_width, len(instances) * config.width_per_instance)
    fig, ax = plt.subplots(figsize=(fig_width, config.height))

    x = np.arange(len(instances))
    width = config.bar_width_ratio / len(agents)
    colors = plt.cm.tab10(np.linspace(0, 1, len(agents)))

    for i, agent in enumerate(agents):
        values = []
        validity_statuses = []

        for instance in instances:
            agent_data = data.get_agent_data(instance, agent)
            if agent_data:
                values.append(getattr(agent_data, metric_key))
                validity_statuses.append(agent_data.validity_status)
            else:
                values.append(0)
                validity_statuses.append(ValidityStatus.VALID)

        bars = ax.bar(x + i * width, values, width, label=agent, color=colors[i], alpha=config.bar_alpha)

        # Apply hatching based on validity status
        for bar, status in zip(bars, validity_statuses):
            if status == ValidityStatus.INVALID_TESTS:
                bar.set_hatch(config.hatch_pattern)
                bar.set_edgecolor(config.invalid_tests_edge_color)
                bar.set_linewidth(config.edge_linewidth)
            elif status == ValidityStatus.NO_EXEC_ENV:
                bar.set_hatch(config.hatch_pattern)
                bar.set_edgecolor(config.no_exec_env_edge_color)
                bar.set_linewidth(config.edge_linewidth)
            elif status == ValidityStatus.NO_TEST_RESULTS:
                bar.set_hatch(config.hatch_pattern)
                bar.set_edgecolor(config.no_test_results_edge_color)
                bar.set_linewidth(config.edge_linewidth)

    # Configure axes
    ax.set_xlabel("Instance (owner/repo/hash)", fontsize=config.xlabel_fontsize)
    ax.set_ylabel("IFR (%)", fontsize=config.ylabel_fontsize)
    ax.set_title(title, fontsize=config.title_fontsize, fontweight="bold")
    ax.set_xticks(x + width * (len(agents) - 1) / 2)
    ax.set_xticklabels(instances, rotation=45, ha="right", fontsize=config.tick_fontsize)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=config.legend_fontsize)
    ax.grid(axis="y", alpha=config.grid_alpha, linestyle=config.grid_linestyle)

    # Add footer text
    fig.text(0.99, 0.01, config.footer_text, ha="right", va="bottom", fontsize=config.footer_fontsize, style="italic")

    plt.tight_layout()
    return fig


def create_ifr_plots(data: AnalysisData, output_dir: Path, config: IFRPlotConfig = IFRPlotConfig(), dpi: int = 300):
    """
    Generate and save all three IFR plots.

    Args:
        data: Analysis data to plot
        output_dir: Directory to save plots
        config: Plot configuration settings
        dpi: Resolution for saved plots
    """
    output_dir.mkdir(exist_ok=True)

    for metric_key, title in IFR_PLOT_DEFINITIONS:
        print(f"  - {title}")
        fig = create_ifr_plot(data, metric_key, title, config)

        output_file = output_dir / f"{metric_key}_plot.png"
        fig.savefig(output_file, dpi=dpi, bbox_inches="tight")
        print(f"    Saved to {output_file}")
        plt.close(fig)
