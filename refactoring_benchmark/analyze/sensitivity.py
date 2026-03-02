"""Sensitivity analysis for pass rate as a function of alpha."""

from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from refactoring_benchmark.analyze.config import PlotConfig
from refactoring_benchmark.analyze.filters import ResultFilter
from refactoring_benchmark.analyze.plotting import (
    AGENT_NAME_MAPPING,
    _apply_science_style,
)
from refactoring_benchmark.analyze.validation import ValidityStatus, check_test_validity
from refactoring_benchmark.evaluation.models import EvaluationResult


def alpha_grid(start: float = 0.0, end: float = 1.0, step: float = 0.01) -> list[float]:
    """Build an inclusive alpha grid."""
    if step <= 0:
        raise ValueError(f"alpha step must be > 0, got {step}")
    if not (0 <= start <= 1 and 0 <= end <= 1):
        raise ValueError(f"alpha start/end must be in [0, 1], got start={start}, end={end}")
    if start > end:
        raise ValueError(f"alpha start must be <= end, got start={start}, end={end}")

    values: list[float] = []
    current = start
    while current <= end + 1e-12:
        values.append(round(current, 10))
        current += step
    return values


def compute_pass_rate_sensitivity(
    results: Sequence[EvaluationResult],
    alphas: Sequence[float],
    filters: Sequence[ResultFilter] | None = None,
) -> dict[str, list[tuple[float, float]]]:
    """Compute pass rate per agent for each alpha."""
    filtered_results: list[EvaluationResult] = []
    for result in results:
        if filters and not all(filter_fn(result) for filter_fn in filters):
            continue
        filtered_results.append(result)

    agent_ids = sorted({r.agent_config.id for r in filtered_results})
    sensitivity: dict[str, list[tuple[float, float]]] = {}

    for agent_id in agent_ids:
        agent_results = [r for r in filtered_results if r.agent_config.id == agent_id]
        points: list[tuple[float, float]] = []
        for alpha in alphas:
            if not agent_results:
                points.append((alpha, 0.0))
                continue
            valid_count = sum(1 for r in agent_results if check_test_validity(r, alpha=alpha) == ValidityStatus.VALID)
            pass_rate = valid_count / len(agent_results)
            points.append((alpha, pass_rate))
        sensitivity[agent_id] = points

    return sensitivity


def create_sensitivity_plot(
    sensitivity_data: dict[str, list[tuple[float, float]]],
    config: PlotConfig = PlotConfig(),
) -> plt.Figure:
    """Create a line chart of pass-rate sensitivity vs alpha."""
    if not sensitivity_data:
        raise ValueError("No sensitivity data to plot")

    _apply_science_style()
    fig, ax = plt.subplots(figsize=(config.width, config.height))

    agents = list(sensitivity_data.keys())
    colors = sns.color_palette("pastel", len(agents))

    for i, agent_id in enumerate(agents):
        points = sensitivity_data[agent_id]
        x = [p[0] for p in points]
        y = [p[1] * 100 for p in points]

        ax.plot(
            x,
            y,
            label=agent_id,
            color=colors[i],
            linestyle="--",
            linewidth=config.line_width,
            alpha=config.alpha,
        )

    ax.set_xlabel(r"$\alpha$")
    if config.show_ylabel:
        ax.set_ylabel(r"\textsc{Pass} (\%)")

    all_x = sorted({alpha for points in sensitivity_data.values() for alpha, _ in points})
    if not all_x:
        raise ValueError("No alpha values to plot")
    ax.set_xlim(min(all_x), max(all_x))
    tick_start = np.floor(min(all_x) * 10) / 10
    tick_end = np.ceil(max(all_x) * 10) / 10
    ax.set_xticks(np.arange(tick_start, tick_end + 1e-12, 0.1))
    ax.set_ylim(config.ylim_min * 100, config.ylim_max * 100)
    ytick_step = config.ytick_step
    ax.set_yticks(np.arange(config.ylim_min * 100, config.ylim_max * 100 + ytick_step * 0.5, ytick_step))

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
        elif config.legend_position == "lower_right":
            legend_kwargs.update({"loc": "lower right"})
        elif config.legend_position == "lower_left":
            legend_kwargs.update({"loc": "lower left"})
        else:
            legend_kwargs.update({"loc": "upper left"})
        ax.legend(**legend_kwargs)

    fig.tight_layout()
    return fig


def save_sensitivity_plot(fig: plt.Figure, output_path: Path) -> None:
    """Save sensitivity plot as PDF."""
    pdf_path = output_path.with_suffix(".pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.close(fig)
