"""Generate plots comparing agents across description types and modes."""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from refactoring_benchmark.analyze.config import PlotConfig, PlotType
from refactoring_benchmark.analyze.models import AggregationType, AnalysisData


# setup
def _apply_science_style():
    mpl.rcParams.update(
        {
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": ["Computer Modern Roman"],
            "font.size": 19,
            "axes.titlesize": 19,
            "axes.labelsize": 17,
            "legend.fontsize": 12,
            "xtick.labelsize": 17,
            "ytick.labelsize": 17,
            "xtick.major.pad": 8,
            # Figure geometry
            "figure.figsize": (3.25, 2.2),
            "figure.dpi": 300,
            # Aesthetics
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.15,
            "grid.linestyle": "--",
        }
    )


_apply_science_style()

METRIC_LABELS = {
    "f1": r"F$_1$ Score",
    "ifr": r"\textsc{Ifr} (\%)",
    "ifr_x_test_success": r"$\mathcal{A}$ (\%)",
    "ifr_added_x_test_success": r"\mathcal{A}^{+} (\%)",
    "ifr_removed_x_test_success": r"\mathcal{A}^{-} (\%)",
    "strict_ifr_x_test_success": "Strict Success Rate",
    "total_score": "Total Score",
    "ifr_added": r"\textsc{Ifr}$^{+}$ (\%)",
    "ifr_removed": r"\textsc{Ifr}$^{-}$ (\%)",
    "ifr_ratio": r"\textsc{Ifr}$_{-}$ / (\textsc{Ifr}$_{+}$ + \textsc{Ifr}$_{-}$) (\%)",
    "diff_added_lines": "Lines Added",
    "diff_removed_lines": "Lines Removed",
    "diff_delta_lines": r"$\Delta$ Lines",
    "test_success": r"\textsc{Pass} (\%)",
    "precision_added": r"\textsc{Prec}$^{+}$ (\%)",
    "precision_removed": r"\textsc{Prec}$^{-}$ (\%)",
    "precision_overall": r"\textsc{Prec} (\%)",
    "cost": "Cost (USD)",
}

AGENT_NAME_MAPPING = {
    "claude-code-v2.0.76-sonnet45": "Sonnet 4.5",
    "codex-v0.77.0-gpt-5.1-codex-mini": "GPT-5.1 M",
    "codex-v0.77.0-gpt-5.2": "GPT-5.2",
    "golden_agent": "Golden",
    "null_agent": "Null",
    "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct": "Qwen3",
}


def create_plot(
    data: AnalysisData,
    metric_name: str,
    plot_type: PlotType = "line",
    aggregation: AggregationType = "mean",
    config: PlotConfig = PlotConfig(),
) -> plt.Figure:
    agents = data.get_agent_ids()
    type_mode_pairs, mapped_labels = data.get_type_mode_pairs_with_labels()

    if not agents or not type_mode_pairs:
        raise ValueError("No data to plot")

    # Dynamic width for bar plots to keep bars equal width
    fig_width = (len(type_mode_pairs) * 1.1 + 2.0) if plot_type == "bar" else config.width
    fig, ax = plt.subplots(figsize=(fig_width, config.height))

    # 1. Labels and Colors
    display_metric = METRIC_LABELS.get(metric_name, metric_name.replace("_", " ").title())
    # Using 'turbo' for a bright, high-contrast spectrum
    colors = sns.color_palette("pastel", len(agents))
    markers = ["o", "s", "^", "D", "v", "p", "*", "h"]

    # 2. Plotting logic
    if plot_type == "line":
        _plot_line(ax, data, agents, type_mode_pairs, colors, aggregation, config, markers)
    elif plot_type == "bar":
        _plot_bar(ax, data, agents, type_mode_pairs, colors, aggregation, config, markers)
    elif plot_type == "scatter":
        _plot_scatter(ax, data, agents, type_mode_pairs, colors, aggregation, config, markers)

    # 3. Axis Configuration
    if config.show_ylabel:
        ax.set_ylabel(f"{display_metric}")

    # 4. Legend with Mapped Names
    if config.show_legend:
        handles, labels = ax.get_legend_handles_labels()
        mapped_agent_labels = [AGENT_NAME_MAPPING.get(label, label) for label in labels]

        legend_kwargs = {
            "handles": handles,
            "labels": mapped_agent_labels,
            "frameon": True,
            "framealpha": 0.7,
            "edgecolor": "none",
            "fontsize": 17,
            "handletextpad": 0.5,
            "markerscale": 0.3,
            "handlelength": 0.5,
        }

        if config.legend_position == "upper_right":
            legend_kwargs.update({"loc": "upper right"})
        elif config.legend_position == "lower_left":
            legend_kwargs.update({"loc": "lower left"})
        else:
            legend_kwargs.update({"loc": "upper left"})

        ax.legend(**legend_kwargs)

    # 5. Ticks and Limits
    ylim_max = config.ylim_max * 100 if config.ylim_max else 100
    ax.set_ylim(config.ylim_min * 100, ylim_max)
    ax.set_yticks(np.arange(0, ylim_max + 1, config.ytick_step))

    n_agents = len(agents)
    x_indices = np.arange(len(mapped_labels))

    if plot_type == "bar":
        width = config.bar_width / n_agents
        center_offset = (width * (n_agents - 1)) / 2
        ax.set_xticks(x_indices + center_offset)
    else:
        ax.set_xticks(x_indices)

    if len(mapped_labels) == 1:
        ax.set_xticks([])
        ax.set_xticklabels([])
    else:
        ax.set_xticklabels(mapped_labels, fontsize=config.tick_fontsize)
    fig.tight_layout()

    return fig


def _plot_line(
    ax: plt.Axes,
    data: AnalysisData,
    agents: list[str],
    type_mode_pairs: list[tuple[str, str]],
    colors: np.ndarray,
    aggregation: AggregationType,
    config: PlotConfig,
    markers: list[str],
) -> None:
    x = np.arange(len(type_mode_pairs))

    for i, agent_id in enumerate(agents):
        values, margins = [], []
        # Check for baseline agents to apply dotted style
        is_baseline = any(name in agent_id.lower() for name in ["golden", "null"])
        linestyle = ":" if is_baseline else "-"

        for desc_type, mode in type_mode_pairs:
            agent_desc_data = data.get_data(agent_id, desc_type, mode)
            if agent_desc_data and agent_desc_data.count > 0:
                val = agent_desc_data.mean if aggregation == "mean" else agent_desc_data.median
                values.append(val * 100)
                if config.show_error_bars and aggregation == "mean":
                    low, _ = agent_desc_data.confidence_interval()
                    margins.append((val - low) * 100)
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
            markeredgecolor="white",
            markeredgewidth=0.5,
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
    type_mode_pairs: list[tuple[str, str]],
    colors: np.ndarray,
    aggregation: AggregationType,
    config: PlotConfig,
    markers: list[str],
) -> None:
    x = np.arange(len(type_mode_pairs))
    width = config.bar_width / len(agents)

    for i, agent_id in enumerate(agents):
        values, margins = [], []
        is_baseline = any(name in agent_id.lower() for name in ["golden", "null"])

        for desc_type, mode in type_mode_pairs:
            agent_desc_data = data.get_data(agent_id, desc_type, mode)
            if agent_desc_data and agent_desc_data.count > 0:
                val = agent_desc_data.mean if aggregation == "mean" else agent_desc_data.median
                values.append(val * 100)
                if config.show_error_bars and aggregation == "mean":
                    low, _ = agent_desc_data.confidence_interval()
                    margins.append((val - low) * 100)
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
    type_mode_pairs: list[tuple[str, str]],
    colors: np.ndarray,
    aggregation: AggregationType,
    config: PlotConfig,
    markers: list[str],
) -> None:
    x = np.arange(len(type_mode_pairs))

    for i, agent_id in enumerate(agents):
        values, margins = [], []
        for desc_type, mode in type_mode_pairs:
            agent_desc_data = data.get_data(agent_id, desc_type, mode)
            if agent_desc_data and agent_desc_data.count > 0:
                val = agent_desc_data.mean if aggregation == "mean" else agent_desc_data.median
                values.append(val * 100)
                if config.show_error_bars and aggregation == "mean":
                    low, _ = agent_desc_data.confidence_interval()
                    margins.append((val - low) * 100)
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
            edgecolors="white",
            linewidths=0.5,
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
    pdf_path = output_path.with_suffix(".pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.close(fig)
