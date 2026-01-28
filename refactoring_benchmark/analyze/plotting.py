"""Generate plots comparing agents across description types."""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from refactoring_benchmark.analyze.models import AnalysisData, AggregationType
from refactoring_benchmark.analyze.config import PlotConfig, PlotType

import matplotlib as mpl

# setup
def _apply_science_style():
    mpl.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "font.size": 10,
        "axes.titlesize": 10,
        "axes.labelsize": 9,      
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        # Figure geometry
        "figure.figsize": (3.25, 2.5), 
        "figure.dpi": 300,
        # Aesthetics
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.15,
        "grid.linestyle": "--",
    })

_apply_science_style()

METRIC_LABELS = {
    "f1": r"F$_1$ Score",
    "ifr": "IFR (Recall)",
    "ifr_x_test_success": r"IFR $\times$ Test Success",
    "strict_ifr_x_test_success": "Strict Success Rate",
    "total_score": "Total Score",
    "ifr_added": "IFR (Added)",
    "ifr_removed": "IFR (Removed)",
    "ifr_ratio": "IFR Removal Ratio",
    "diff_added_lines": "Lines Added",
    "diff_removed_lines": "Lines Removed",
    "diff_delta_lines": r"$\Delta$ Lines",
    "test_success": "Test Pass Rate",
    "precision_added": "Precision (Added)",
    "precision_removed": "Precision (Removed)",
    "precision_overall": "Overall Precision",
    "cost": "Cost (USD)"
}

DESC_TYPE_MAPPING = {
    "standard": "Detailed",
    "abstract": "Abstract",
    "abstract_plan": "Abstract (Plan)",
    "abstract_multiplan": "Abstract (Multiplan)",
    "open": "Open"
}

AGENT_NAME_MAPPING = {
    "claude-code-v2.0.76-sonnet45": "Claude Sonnet 4.5",
    "codex-v0.77.0-gpt-5.1-codex-mini": "GPT-5.1 Codex Mini",
    "codex-v0.77.0-gpt-5.2": "GPT-5.2 Codex",
    "golden_agent": "Golden",
    "null_agent": "Null",
    "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct": "Qwen3 Coder 30B"
}

def create_plot(
    data: AnalysisData,
    metric_name: str,
    plot_type: PlotType = "line",
    aggregation: AggregationType = "mean",
    config: PlotConfig = PlotConfig(),
) -> plt.Figure:
    agents = data.get_agent_ids()
    description_types = data.get_description_types()

    if not agents or not description_types:
        raise ValueError("No data to plot")

    fig, ax = plt.subplots(figsize=(config.width, config.height))
    
    # 1. Labels and Colors
    display_metric = METRIC_LABELS.get(metric_name, metric_name.replace("_", " ").title())
    mapped_labels = [DESC_TYPE_MAPPING.get(t, t) for t in description_types]
    
    # Using 'turbo' for a bright, high-contrast spectrum
    colors = sns.color_palette("pastel", len(agents))
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h']
    
    # 2. Plotting logic
    if plot_type == "line":
        _plot_line(ax, data, agents, description_types, colors, aggregation, config, markers)
    elif plot_type == "bar":
        _plot_bar(ax, data, agents, description_types, colors, aggregation, config, markers)
    elif plot_type == "scatter":
        _plot_scatter(ax, data, agents, description_types, colors, aggregation, config, markers)

    # 3. Axis Configuration
    ax.set_xlabel(r"\textbf{Description Type}", labelpad=8)
    ax.set_ylabel(f"{display_metric}")
    
    # 4. Legend with Mapped Names
    handles, labels = ax.get_legend_handles_labels()
    mapped_agent_labels = [AGENT_NAME_MAPPING.get(l, l) for l in labels]
    
    ax.legend(
        handles,
        mapped_agent_labels,
        loc="best", 
        frameon=True,
        framealpha=0.9, 
        edgecolor='none', 
        fontsize=9,
        handletextpad=0.5
    )

    # 5. Ticks and Limits
    ax.set_ylim(config.ylim_min, config.ylim_max * 1.05 if config.ylim_max else 1.1)
    
    n_agents = len(agents)
    x_indices = np.arange(len(mapped_labels))
    
    if plot_type == "bar":
        width = config.bar_width / n_agents
        center_offset = (width * (n_agents - 1)) / 2
        ax.set_xticks(x_indices + center_offset)
    else:
        ax.set_xticks(x_indices)
        
    ax.set_xticklabels(mapped_labels, fontsize=config.tick_fontsize)
    fig.tight_layout()
    
    return fig


def _plot_line(
    ax: plt.Axes,
    data: AnalysisData,
    agents: list[str],
    description_types: list[str],
    colors: np.ndarray,
    aggregation: AggregationType,
    config: PlotConfig,
    markers: list[str],
) -> None:
    x = np.arange(len(description_types))

    for i, agent_id in enumerate(agents):
        values, margins = [], []
        # Check for baseline agents to apply dotted style
        is_baseline = any(name in agent_id.lower() for name in ["golden", "null"])
        linestyle = ":" if is_baseline else "-"

        for desc_type in description_types:
            agent_desc_data = data.get_data(agent_id, desc_type)
            if agent_desc_data and agent_desc_data.count > 0:
                val = agent_desc_data.mean if aggregation == "mean" else agent_desc_data.median
                values.append(val)
                if config.show_error_bars and aggregation == "mean":
                    low, _ = agent_desc_data.confidence_interval()
                    margins.append(val - low)
                else:
                    margins.append(0.0)
            else:
                values.append(np.nan)
                margins.append(np.nan)

        ax.plot(
            x,
            values,
            label=agent_id,
            color=colors[i],
            linestyle=linestyle,
            linewidth=config.line_width,
            marker=markers[i % len(markers)],
            markersize=config.marker_size,
            alpha=config.alpha,
            markeredgecolor='white',
            markeredgewidth=0.5
        )

        if config.show_error_bars:
            ax.errorbar(
                x,
                values,
                yerr=margins,
                fmt="none",
                ecolor=colors[i],
                capsize=config.error_bar_capsize,
                alpha=config.error_bar_alpha,
            )


def _plot_bar(
    ax: plt.Axes,
    data: AnalysisData,
    agents: list[str],
    description_types: list[str],
    colors: np.ndarray,
    aggregation: AggregationType,
    config: PlotConfig,
    markers: list[str],
) -> None:
    x = np.arange(len(description_types))
    width = config.bar_width / len(agents)

    for i, agent_id in enumerate(agents):
        values, margins = [], []
        is_baseline = any(name in agent_id.lower() for name in ["golden", "null"])

        for desc_type in description_types:
            agent_desc_data = data.get_data(agent_id, desc_type)
            if agent_desc_data and agent_desc_data.count > 0:
                val = agent_desc_data.mean if aggregation == "mean" else agent_desc_data.median
                values.append(val)
                if config.show_error_bars and aggregation == "mean":
                    low, _ = agent_desc_data.confidence_interval()
                    margins.append(val - low)
                else:
                    margins.append(0.0)
            else:
                values.append(0.0)
                margins.append(0.0)

        ax.bar(
            x + i * width,
            values,
            width,
            label=agent_id,
            color=colors[i],
            alpha=config.bar_alpha,
            yerr=margins if config.show_error_bars else None,
            capsize=config.error_bar_capsize,
            # Dotted border for baseline agents
            edgecolor="black" if is_baseline else "none",
            linestyle=":" if is_baseline else "-",
            linewidth=0.8 if is_baseline else 0,
            error_kw={"alpha": config.error_bar_alpha},
        )


def _plot_scatter(
    ax: plt.Axes,
    data: AnalysisData,
    agents: list[str],
    description_types: list[str],
    colors: np.ndarray,
    aggregation: AggregationType,
    config: PlotConfig,
    markers: list[str],
) -> None:
    x = np.arange(len(description_types))

    for i, agent_id in enumerate(agents):
        values, margins = [], []
        for desc_type in description_types:
            agent_desc_data = data.get_data(agent_id, desc_type)
            if agent_desc_data and agent_desc_data.count > 0:
                val = agent_desc_data.mean if aggregation == "mean" else agent_desc_data.median
                values.append(val)
                if config.show_error_bars and aggregation == "mean":
                    low, _ = agent_desc_data.confidence_interval()
                    margins.append(val - low)
                else:
                    margins.append(0.0)
            else:
                values.append(np.nan)
                margins.append(np.nan)

        x_pos = x + (i - len(agents) / 2) * 0.1
        ax.scatter(
            x_pos,
            values,
            label=agent_id,
            color=colors[i],
            s=config.marker_size**2,
            marker=markers[i % len(markers)],
            alpha=config.alpha,
            zorder=3,
            edgecolors='white',
            linewidths=0.5
        )

        if config.show_error_bars:
            ax.errorbar(
                x_pos,
                values,
                yerr=margins,
                fmt="none",
                ecolor=colors[i],
                capsize=config.error_bar_capsize,
                alpha=config.error_bar_alpha,
                zorder=2,
            )


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
