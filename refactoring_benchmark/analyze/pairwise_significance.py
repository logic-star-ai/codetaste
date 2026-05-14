#!/usr/bin/env python3
"""Pairwise statistical significance analysis for benchmark model comparisons."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from refactoring_benchmark.analyze.loader import (
    discover_output_dirs,
    load_all_results,
    organize_data,
)
from refactoring_benchmark.analyze.models import (
    DESC_TYPE_LABELS,
    MODE_LABELS,
    AgentDescriptionData,
    sort_type_mode_pairs,
)
from refactoring_benchmark.analyze.statistics import LATEX_AGENT_NAME_MAPPING
from refactoring_benchmark.utils.common import load_instances_from_csv

DEFAULT_METRICS = ("ifr", "test_success", "ifr_x_test_success")
DEFAULT_ALPHA = 0.05
DEFAULT_PERMUTATIONS = 100_000
DEFAULT_BOOTSTRAP_RESAMPLES = 10_000
DEFAULT_EXACT_THRESHOLD = 16
DEFAULT_SEED = 0
ZERO_TOLERANCE = 1e-12
REPORT_JSON = "pairwise_significance.json"
REPORT_MD = "pairwise_significance.md"
REPORT_MERMAID_MD = "pairwise_significance_mermaid.md"
REPORT_LATEX_SUMMARY = "pairwise_significance_summary.tex"
DEFAULT_REPORT_DIR = Path("plots/pairwise_significance")
EXCLUDED_AGENT_IDS = {"golden_agent", "null_agent"}
SUMMARY_AGENT_ORDER = (
    "codex-v0.77.0-gpt-5.2",
    "codex-v0.77.0-gpt-5.1-codex-mini",
    "claude-code-v2.0.76-sonnet45",
    "claude-code-v2.1.71-minimax-m2.7",
    "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct",
)
LATEX_SUMMARY_AGENT_LABELS = {
    "codex-v0.77.0-gpt-5.2": "GPT-5.2",
    "codex-v0.77.0-gpt-5.1-codex-mini": "GPT-5.1 Mini",
    "claude-code-v2.0.76-sonnet45": "Sonnet 4.5",
    "claude-code-v2.1.71-minimax-m2.7": "MiniMax",
    "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct": "Qwen3",
}


@dataclass(frozen=True)
class PairwisePoint:
    """Aligned metric values for one shared benchmark instance."""

    instance_key: str
    value_a: float
    value_b: float

    @property
    def difference(self) -> float:
        return self.value_a - self.value_b


@dataclass
class PairwiseComparison:
    """Pairwise significance result for one metric and one type/mode slice."""

    metric: str
    description_type: str
    mode: str
    model_a: str
    model_b: str
    better_model: str | None
    worse_model: str | None
    observed_n_pairs: int
    n_pairs: int
    n_nonzero_differences: int
    mean_a: float
    mean_b: float
    mean_difference: float
    ci_low: float
    ci_high: float
    wins_a: int
    ties: int
    wins_b: int
    p_value: float
    q_value: float | None
    alpha: float
    is_significant: bool
    test: str
    observed_direction: str
    permutation_method: str
    permutations: int
    bootstrap_resamples: int

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["description_type_label"] = DESC_TYPE_LABELS.get(self.description_type, self.description_type)
        payload["mode_label"] = MODE_LABELS.get(self.mode, self.mode)
        payload["model_a_label"] = display_agent_name(self.model_a)
        payload["model_b_label"] = display_agent_name(self.model_b)
        payload["better_model_label"] = display_agent_name(self.better_model) if self.better_model else None
        payload["worse_model_label"] = display_agent_name(self.worse_model) if self.worse_model else None
        return payload


def display_agent_name(agent_id: str | None) -> str | None:
    """Convert internal agent IDs to paper-friendly names when available."""
    if agent_id is None:
        return None
    return LATEX_AGENT_NAME_MAPPING.get(agent_id, agent_id)


def stable_seed(*parts: object, base_seed: int) -> int:
    """Derive a deterministic 32-bit seed from comparison identity fields."""
    payload = "|".join(map(str, (*parts, base_seed)))
    digest = hashlib.sha256(payload.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % (2**32)


def filter_results(
    results: Sequence[Any],
    *,
    agent_ids: Sequence[str] | None = None,
    description_types: Sequence[str] | None = None,
    modes: Sequence[str] | None = None,
    successful_only: bool = False,
) -> list[Any]:
    """Filter evaluation results using the subset of fields needed for statistics."""
    agent_filter = set(agent_ids or [])
    desc_filter = set(description_types or [])
    mode_filter = set(modes or [])

    filtered: list[Any] = []
    for result in results:
        agent_id = result.agent_config.id
        if agent_id in EXCLUDED_AGENT_IDS:
            continue
        metadata = result.inference_metadata
        description_type = metadata.description_type if metadata else None
        mode = metadata.mode if metadata else None
        finish_reason = metadata.finish_reason if metadata else None

        if agent_filter and agent_id not in agent_filter:
            continue
        if desc_filter and description_type not in desc_filter:
            continue
        if mode_filter and mode not in mode_filter:
            continue
        if successful_only and finish_reason != "success":
            continue
        filtered.append(result)
    return filtered


def align_paired_points(data_a: AgentDescriptionData, data_b: AgentDescriptionData) -> list[PairwisePoint]:
    """Align two model outputs on their shared instance keys."""
    values_a = _unique_metric_values(data_a)
    values_b = _unique_metric_values(data_b)
    shared_keys = sorted(values_a.keys() & values_b.keys())
    aligned: list[PairwisePoint] = []
    for key in shared_keys:
        value_a = float(values_a[key])
        value_b = float(values_b[key])
        if not math.isfinite(value_a) or not math.isfinite(value_b):
            raise ValueError(f"Non-finite metric value for instance {key}: {value_a}, {value_b}")
        aligned.append(PairwisePoint(instance_key=key, value_a=value_a, value_b=value_b))
    return aligned


def _unique_metric_values(data: AgentDescriptionData) -> dict[str, float]:
    """Return metric values keyed by instance, failing on duplicate paired-test inputs."""
    values: dict[str, float] = {}
    for point in data.metric_values:
        if point.instance_key in values:
            raise ValueError(
                f"Duplicate metric value for agent {data.agent_id} in {data.description_type}/{data.mode}: "
                f"{point.instance_key}"
            )
        values[point.instance_key] = float(point.value)
    return values


def paired_permutation_p_value(
    differences: Sequence[float],
    *,
    alternative: str = "two-sided",
    permutations: int = DEFAULT_PERMUTATIONS,
    exact_threshold: int = DEFAULT_EXACT_THRESHOLD,
    seed: int = DEFAULT_SEED,
) -> tuple[float, str, int]:
    """Run a paired sign-flip permutation test on a vector of paired differences."""
    if alternative not in {"greater", "less", "two-sided"}:
        raise ValueError(f"Unsupported alternative: {alternative}")

    diffs = np.asarray(differences, dtype=float)
    diffs = diffs[~np.isclose(diffs, 0.0, atol=ZERO_TOLERANCE, rtol=0.0)]
    n = int(diffs.size)
    if n == 0:
        return 1.0, "degenerate_all_ties", 0

    observed_sum = float(diffs.sum())
    observed = abs(observed_sum) if alternative == "two-sided" else observed_sum

    if n <= exact_threshold:
        extreme = 0
        total = 1 << n
        for mask in range(total):
            signs = np.ones(n, dtype=float)
            for bit in range(n):
                if (mask >> bit) & 1:
                    signs[bit] = -1.0
            statistic = float(np.dot(signs, diffs))
            if alternative == "two-sided":
                is_extreme = abs(statistic) >= observed - ZERO_TOLERANCE
            elif alternative == "greater":
                is_extreme = statistic >= observed - ZERO_TOLERANCE
            else:
                is_extreme = statistic <= observed + ZERO_TOLERANCE
            if is_extreme:
                extreme += 1
        return extreme / total, "exact", total

    rng = np.random.default_rng(seed)
    sign_matrix = rng.choice(np.array([-1.0, 1.0]), size=(permutations, n))
    statistics = sign_matrix @ diffs
    if alternative == "two-sided":
        extreme = int(np.count_nonzero(np.abs(statistics) >= observed - ZERO_TOLERANCE))
    elif alternative == "greater":
        extreme = int(np.count_nonzero(statistics >= observed - ZERO_TOLERANCE))
    else:
        extreme = int(np.count_nonzero(statistics <= observed + ZERO_TOLERANCE))
    return (extreme + 1) / (permutations + 1), "monte_carlo", permutations


def paired_bootstrap_mean_ci(
    differences: Sequence[float],
    *,
    confidence: float = 0.95,
    resamples: int = DEFAULT_BOOTSTRAP_RESAMPLES,
    seed: int = DEFAULT_SEED,
) -> tuple[float, float]:
    """Bootstrap a confidence interval for the paired mean difference."""
    diffs = np.asarray(differences, dtype=float)
    n = int(diffs.size)
    if n == 0:
        return math.nan, math.nan
    if n == 1:
        value = float(diffs[0])
        return value, value

    rng = np.random.default_rng(seed)
    sample_indices = rng.integers(0, n, size=(resamples, n))
    bootstrap_means = diffs[sample_indices].mean(axis=1)
    alpha = 1.0 - confidence
    low = float(np.quantile(bootstrap_means, alpha / 2.0))
    high = float(np.quantile(bootstrap_means, 1.0 - alpha / 2.0))
    return low, high


def apply_benjamini_hochberg(p_values: Sequence[float]) -> list[float]:
    """Apply Benjamini-Hochberg FDR correction."""
    if not p_values:
        return []

    indexed = sorted(enumerate(p_values), key=lambda item: item[1])
    m = len(indexed)
    adjusted = [0.0] * m
    running_min = 1.0

    for reverse_rank, (original_index, p_value) in enumerate(reversed(indexed), start=1):
        rank = m - reverse_rank + 1
        candidate = min(1.0, p_value * m / rank)
        running_min = min(running_min, candidate)
        adjusted[original_index] = running_min
    return adjusted


def analyze_metric_significance(
    analysis_data: Any,
    *,
    metric: str,
    alpha: float = DEFAULT_ALPHA,
    permutations: int = DEFAULT_PERMUTATIONS,
    bootstrap_resamples: int = DEFAULT_BOOTSTRAP_RESAMPLES,
    exact_threshold: int = DEFAULT_EXACT_THRESHOLD,
    seed: int = DEFAULT_SEED,
) -> list[PairwiseComparison]:
    """Compute all pairwise model comparisons for one metric."""
    comparisons: list[PairwiseComparison] = []
    for description_type, mode in sort_type_mode_pairs(analysis_data.get_type_mode_pairs()):
        slice_agents: list[str] = []
        for agent_id in analysis_data.get_agent_ids():
            agent_slice = analysis_data.get_data(agent_id, description_type, mode)
            if agent_slice and agent_slice.count > 0:
                slice_agents.append(agent_id)

        for model_a, model_b in itertools.combinations(slice_agents, 2):
            data_a = analysis_data.get_data(model_a, description_type, mode)
            data_b = analysis_data.get_data(model_b, description_type, mode)
            if data_a is None or data_b is None:
                continue

            observed_aligned = align_paired_points(data_a, data_b)
            if not observed_aligned:
                continue
            aligned = observed_aligned
            comparison_seed = stable_seed(
                metric,
                description_type,
                mode,
                model_a,
                model_b,
                base_seed=seed,
            )

            differences = np.asarray([point.difference for point in aligned], dtype=float)
            mean_difference = float(differences.mean())
            ci_low, ci_high = paired_bootstrap_mean_ci(
                differences,
                resamples=bootstrap_resamples,
                seed=comparison_seed,
            )

            wins_a = int(np.count_nonzero(differences > ZERO_TOLERANCE))
            wins_b = int(np.count_nonzero(differences < -ZERO_TOLERANCE))
            ties = int(np.count_nonzero(np.isclose(differences, 0.0, atol=ZERO_TOLERANCE, rtol=0.0)))
            n_nonzero = wins_a + wins_b

            if mean_difference > ZERO_TOLERANCE:
                better_model = model_a
                worse_model = model_b
                direction = f"{model_a} > {model_b}"
            elif mean_difference < -ZERO_TOLERANCE:
                better_model = model_b
                worse_model = model_a
                direction = f"{model_b} > {model_a}"
            else:
                better_model = None
                worse_model = None
                p_value = 1.0
                method = "zero_mean_difference"
                realized_permutations = 0
                direction = "tie"

            if not np.isclose(mean_difference, 0.0, atol=ZERO_TOLERANCE, rtol=0.0):
                p_value, method, realized_permutations = paired_permutation_p_value(
                    differences,
                    alternative="two-sided",
                    permutations=permutations,
                    exact_threshold=exact_threshold,
                    seed=comparison_seed,
                )

            comparisons.append(
                PairwiseComparison(
                    metric=metric,
                    description_type=description_type,
                    mode=mode,
                    model_a=model_a,
                    model_b=model_b,
                    better_model=better_model,
                    worse_model=worse_model,
                    observed_n_pairs=len(observed_aligned),
                    n_pairs=len(aligned),
                    n_nonzero_differences=n_nonzero,
                    mean_a=float(np.mean([point.value_a for point in aligned])),
                    mean_b=float(np.mean([point.value_b for point in aligned])),
                    mean_difference=mean_difference,
                    ci_low=ci_low,
                    ci_high=ci_high,
                    wins_a=wins_a,
                    ties=ties,
                    wins_b=wins_b,
                    p_value=float(p_value),
                    q_value=None,
                    alpha=alpha,
                    is_significant=False,
                    test="paired_sign_flip_permutation",
                    observed_direction=direction,
                    permutation_method=method,
                    permutations=realized_permutations,
                    bootstrap_resamples=bootstrap_resamples,
                )
            )

    q_values = apply_benjamini_hochberg([comparison.p_value for comparison in comparisons])
    for comparison, q_value in zip(comparisons, q_values):
        comparison.q_value = float(q_value)
        comparison.is_significant = (
            comparison.better_model is not None
            and comparison.q_value <= alpha
            and not np.isclose(comparison.mean_difference, 0.0, atol=ZERO_TOLERANCE, rtol=0.0)
        )
    return comparisons


def build_report(
    *,
    output_dirs: Sequence[Path],
    instances_csv: Path,
    metrics: Sequence[str] = DEFAULT_METRICS,
    agent_ids: Sequence[str] | None = None,
    description_types: Sequence[str] | None = None,
    modes: Sequence[str] | None = None,
    successful_only: bool = False,
    alpha: float = DEFAULT_ALPHA,
    permutations: int = DEFAULT_PERMUTATIONS,
    bootstrap_resamples: int = DEFAULT_BOOTSTRAP_RESAMPLES,
    exact_threshold: int = DEFAULT_EXACT_THRESHOLD,
    seed: int = DEFAULT_SEED,
) -> dict[str, Any]:
    """Load benchmark outputs and build pairwise significance tables."""
    instances = load_instances_from_csv(instances_csv)
    results = load_all_results(list(output_dirs), instances, agent_ids=agent_ids)
    results = filter_results(
        results,
        agent_ids=agent_ids,
        description_types=description_types,
        modes=modes,
        successful_only=successful_only,
    )

    metric_reports: dict[str, list[PairwiseComparison]] = {}
    for metric in metrics:
        analysis_data = organize_data(results, metric)
        if agent_ids:
            analysis_data = analysis_data.filter_agents(list(agent_ids))
        if description_types:
            analysis_data = analysis_data.filter_description_types(list(description_types))
        if modes:
            analysis_data = analysis_data.filter_modes(list(modes))
        metric_reports[metric] = analyze_metric_significance(
            analysis_data,
            metric=metric,
            alpha=alpha,
            permutations=permutations,
            bootstrap_resamples=bootstrap_resamples,
            exact_threshold=exact_threshold,
            seed=seed,
        )

    metadata = {
        "metrics": list(metrics),
        "alpha": alpha,
        "permutations": permutations,
        "bootstrap_resamples": bootstrap_resamples,
        "exact_threshold": exact_threshold,
        "seed": seed,
        "successful_only": successful_only,
        "output_dirs": [str(path) for path in output_dirs],
        "instances_csv": str(instances_csv),
        "agent_ids": list(agent_ids) if agent_ids else None,
        "description_types": list(description_types) if description_types else None,
        "modes": list(modes) if modes else None,
        "n_results_after_filtering": len(results),
    }

    return {
        "metadata": metadata,
        "metrics": {metric: [comparison.to_dict() for comparison in comparisons] for metric, comparisons in metric_reports.items()},
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    """Render a human-readable markdown summary."""
    lines: list[str] = ["# Pairwise Significance Report", ""]
    metadata = report["metadata"]
    lines.append(f"- Metrics: {', '.join(metadata['metrics'])}")
    lines.append(f"- Alpha: {metadata['alpha']:.3f}")
    lines.append(f"- Result rows after filtering: {metadata['n_results_after_filtering']}")
    if metadata["successful_only"]:
        lines.append("- Included only `finish_reason=success` runs")
    lines.append("")
    lines.extend(render_markdown_summary_table(report))
    lines.append("")
    lines.extend(
        [
            "## Table Guide",
            "",
            "| Column | Meaning |",
            "| --- | --- |",
            "| Model 1 | For non-zero paired mean differences, the model with the larger paired mean. If the paired mean difference is zero, the row falls back to Model A / Model B ordering and no better model is claimed. |",
            "| Model 2 | The other model in the pair. If the paired mean difference is zero, the row falls back to Model A / Model B ordering and no worse model is claimed. |",
            "| N | Number of shared instances used in the paired comparison. Only instances present for both models in that description-type/mode slice are counted. |",
            "| Mean 1 | Mean metric value for Model 1 over those `N` shared instances. |",
            "| Mean 2 | Mean metric value for Model 2 over those `N` shared instances. |",
            "| Delta | Paired mean difference, shown as `Mean 1 - Mean 2`, in percentage points. |",
            "| 95% CI | 95% bootstrap confidence interval for the paired mean difference. |",
            "| W/T/L | Win/Tie/Loss counts over the `N` shared instances from the perspective of Model 1. `W` means Model 1 had the higher per-instance metric value, `T` means both models tied, and `L` means Model 1 lost on that instance. |",
            "| p | Two-sided paired sign-flip permutation-test p-value for the null hypothesis of zero paired mean difference. |",
            "| q | Benjamini-Hochberg false-discovery-rate adjusted p-value, computed across all pairwise comparisons for the same metric. |",
            "| Significant | `yes` if and only if the row has a non-zero paired mean difference and `q <= alpha`; otherwise `no`. |",
            "",
            "## Significance Rule",
            "",
            "A row is called statistically significant when all of the following hold:",
            "",
            "1. The paired mean difference is not zero.",
            f"2. The Benjamini-Hochberg adjusted two-sided paired permutation p-value satisfies `q <= {metadata['alpha']:.3f}`.",
            "",
            "The table is descriptive even when `Significant = no`: the means, delta, confidence interval, and win/tie/loss counts still describe the observed paired sample, but the evidence is not strong enough for a corrected significance claim.",
            "",
        ]
    )

    for metric in metadata["metrics"]:
        comparisons = report["metrics"][metric]
        lines.append(f"## {metric}")
        lines.append("")
        if not comparisons:
            lines.append("No pairwise comparisons available.")
            lines.append("")
            continue

        by_slice: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in comparisons:
            by_slice.setdefault((row["description_type"], row["mode"]), []).append(row)

        for description_type, mode in sort_type_mode_pairs(by_slice.keys()):
            slice_rows = by_slice[(description_type, mode)]
            lines.append(f"### {DESC_TYPE_LABELS.get(description_type, description_type)} / {MODE_LABELS.get(mode, mode)}")
            lines.append("")
            lines.append(
                "| Model 1 | Model 2 | N | Mean 1 | Mean 2 | Delta | 95% CI | W/T/L | p | q | Significant |"
            )
            lines.append("| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |")
            for row in sorted(
                slice_rows,
                key=lambda item: (
                    not item["is_significant"],
                    -(abs(item["mean_difference"])),
                    item["model_a_label"],
                    item["model_b_label"],
                ),
            ):
                model_1 = row["better_model_label"] or row["model_a_label"]
                model_2 = row["worse_model_label"] or row["model_b_label"]
                oriented_delta, ci_low, ci_high, wins, ties, losses = _oriented_summary_fields(row)
                delta_pp = 100.0 * oriented_delta
                ci_low_pp = 100.0 * ci_low
                ci_high_pp = 100.0 * ci_high
                if row["better_model"] == row["model_a"]:
                    mean_1 = row["mean_a"]
                    mean_2 = row["mean_b"]
                elif row["better_model"] == row["model_b"]:
                    mean_1 = row["mean_b"]
                    mean_2 = row["mean_a"]
                else:
                    mean_1 = row["mean_a"]
                    mean_2 = row["mean_b"]
                wins_losses = f"{wins}/{ties}/{losses}"
                lines.append(
                    f"| {model_1} | {model_2} | {row['n_pairs']} | {100.0 * mean_1:.2f}% | "
                    f"{100.0 * mean_2:.2f}% | {delta_pp:.2f} pp | "
                    f"[{ci_low_pp:.2f}, {ci_high_pp:.2f}] pp | {wins_losses} | {row['p_value']:.4g} | "
                    f"{row['q_value']:.4g} | {'yes' if row['is_significant'] else 'no'} |"
                )
            lines.append("")
    return "\n".join(lines)


def build_significance_win_loss_summary(
    report: dict[str, Any],
) -> tuple[list[str], list[dict[str, Any]]]:
    """Summarize significant pairwise wins and losses by metric and setting."""
    all_agents: set[str] = set()
    summary_rows: list[dict[str, Any]] = []

    for metric in report["metadata"]["metrics"]:
        by_slice: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in report["metrics"][metric]:
            by_slice.setdefault((row["description_type"], row["mode"]), []).append(row)

        for description_type, mode in sort_type_mode_pairs(by_slice.keys()):
            slice_rows = by_slice[(description_type, mode)]
            agents = {row["model_a"] for row in slice_rows} | {row["model_b"] for row in slice_rows}
            all_agents.update(agents)
            counts = {agent_id: {"wins": 0, "losses": 0} for agent_id in agents}

            for row in slice_rows:
                if not row["is_significant"] or not row["better_model"] or not row["worse_model"]:
                    continue
                counts[row["better_model"]]["wins"] += 1
                counts[row["worse_model"]]["losses"] += 1

            n_pairs = sorted({int(row["n_pairs"]) for row in slice_rows})
            summary_rows.append(
                {
                    "metric": metric,
                    "description_type": description_type,
                    "mode": mode,
                    "setting_label": _setting_label(description_type, mode),
                    "n_pairs": _format_n_pairs(n_pairs),
                    "counts": counts,
                }
            )

    return _sorted_summary_agents(all_agents), summary_rows


def render_markdown_summary_table(report: dict[str, Any]) -> list[str]:
    """Render a compact paper-oriented table of significant pairwise outcomes."""
    agents, summary_rows = build_significance_win_loss_summary(report)
    if not summary_rows:
        return ["## Paper Summary", "", "No pairwise comparisons available."]

    lines = [
        "## Paper Summary",
        "",
        "Each model cell reports significant pairwise wins/losses against the other models in that metric and setting. "
        f"Significance uses the paired permutation test with Benjamini-Hochberg correction at "
        f"`q <= {report['metadata']['alpha']:.3f}`.",
        "",
    ]
    header = ["Metric", "Setting", "N", *[display_agent_name(agent_id) or agent_id for agent_id in agents]]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---", "---", "---:"] + ["---:"] * len(agents)) + " |")

    for row in summary_rows:
        cells = [f"`{row['metric']}`", row["setting_label"], row["n_pairs"]]
        for agent_id in agents:
            counts = row["counts"].get(agent_id)
            cells.append("--" if counts is None else f"{counts['wins']}/{counts['losses']}")
        lines.append("| " + " | ".join(cells) + " |")

    return lines


def render_latex_summary_table(report: dict[str, Any]) -> str:
    """Render a LaTeX table snippet for the compact significance summary."""
    agents, summary_rows = build_significance_win_loss_summary(report)
    if not summary_rows:
        return "% No pairwise comparisons available.\n"

    column_spec = "llr" + ("c" * len(agents))
    agent_headers = " & ".join(_latex_escape(_latex_summary_agent_label(agent_id)) for agent_id in agents)
    lines = [
        "% Generated by refactoring_benchmark.cli.pairwise_significance.",
        "% Model cells report significant pairwise wins/losses after Benjamini-Hochberg correction.",
        "\\begin{table}",
        "\\centering",
        "\\small",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\begin{tabular}{" + column_spec + "}",
        "\\toprule",
        "Metric & Setting & $N$ & " + agent_headers + " \\\\",
        "\\midrule",
    ]
    for row in summary_rows:
        cells = [
            "\\texttt{" + _latex_escape(row["metric"]) + "}",
            _latex_escape(row["setting_label"]),
            row["n_pairs"],
        ]
        for agent_id in agents:
            counts = row["counts"].get(agent_id)
            cells.append("--" if counts is None else f"{counts['wins']}/{counts['losses']}")
        lines.append(" & ".join(cells) + " \\\\")
    lines.extend(
        [
            "\\bottomrule",
            "\\end{tabular}",
            "\\caption{Pairwise significance summary. Each model cell reports significant wins/losses against the other models in the same metric and setting.}",
            "\\label{tab:pairwise-significance-summary}",
            "\\end{table}",
            "",
        ]
    )
    return "\n".join(lines)


def render_mermaid_report(report: dict[str, Any]) -> str:
    """Render Mermaid diagrams for each metric and setting."""
    lines: list[str] = ["# Pairwise Significance Graphs", ""]
    lines.extend(
        [
            "Each diagram is a directed graph for one `(metric, description_type, mode)` setting.",
            "",
            "- A node is a model.",
            "- An arrow `A --> B` means `A` has the better observed paired mean and the comparison is statistically significant in that setting.",
            "- No arrow means there is no corrected significance claim in that direction.",
            "",
        ]
    )

    for metric in report["metadata"]["metrics"]:
        lines.append(f"## {metric}")
        lines.append("")
        metric_rows = report["metrics"][metric]
        if not metric_rows:
            lines.append("No pairwise comparisons available.")
            lines.append("")
            continue

        by_slice: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in metric_rows:
            by_slice.setdefault((row["description_type"], row["mode"]), []).append(row)

        lines.append("### Combined")
        lines.append("")
        lines.append("```mermaid")
        lines.append(build_combined_mermaid_diagram(metric, by_slice))
        lines.append("```")
        lines.append("")

        for description_type, mode in sort_type_mode_pairs(by_slice.keys()):
            desc_label = DESC_TYPE_LABELS.get(description_type, description_type)
            mode_label = MODE_LABELS.get(mode, mode)
            lines.append(f"### {desc_label} / {mode_label}")
            lines.append("")
            lines.append("```mermaid")
            lines.append(build_mermaid_diagram(metric, description_type, mode, by_slice[(description_type, mode)]))
            lines.append("```")
            lines.append("")

    return "\n".join(lines)


def build_combined_mermaid_diagram(
    metric: str,
    rows_by_slice: dict[tuple[str, str], list[dict[str, Any]]],
) -> str:
    """Build one Mermaid graph per metric with a subgraph for each setting."""
    lines = [
        f"%% {metric}",
        "flowchart TB",
        f'  subgraph {_mermaid_node_id("combined_" + metric)}["{_mermaid_label(metric)}"]',
        "    direction TB",
    ]

    for description_type, mode in sort_type_mode_pairs(rows_by_slice.keys()):
        desc_label = DESC_TYPE_LABELS.get(description_type, description_type)
        mode_label = MODE_LABELS.get(mode, mode)
        slice_id = _mermaid_node_id(f"{metric}_{description_type}_{mode}")
        lines.append(f'    subgraph {slice_id}["{_mermaid_label(f"{desc_label} - {mode_label}")}"]')
        lines.append("      direction LR")

        rows = rows_by_slice[(description_type, mode)]
        node_labels: dict[str, str] = {}
        for row in rows:
            node_labels[row["model_a"]] = row["model_a_label"]
            node_labels[row["model_b"]] = row["model_b_label"]

        for agent_id, label in sorted(node_labels.items(), key=lambda item: item[1]):
            lines.append(
                f'      {_mermaid_node_id(f"{description_type}_{mode}_{agent_id}")}["{_mermaid_label(label)}"]'
            )

        significant_rows = [row for row in rows if row["is_significant"] and row["better_model"] and row["worse_model"]]
        for row in sorted(significant_rows, key=lambda item: (item["better_model_label"], item["worse_model_label"])):
            better_id = _mermaid_node_id(f"{description_type}_{mode}_{row['better_model']}")
            worse_id = _mermaid_node_id(f"{description_type}_{mode}_{row['worse_model']}")
            lines.append(f"      {better_id} --> {worse_id}")

        if not significant_rows:
            lines.append(
                f'      note_{_mermaid_node_id(f"combined_{metric}_{description_type}_{mode}")}'
                f'["{_mermaid_label("No significant pairwise edges")}"]'
            )
        lines.append("    end")

    lines.append("  end")
    return "\n".join(lines)


def build_mermaid_diagram(
    metric: str,
    description_type: str,
    mode: str,
    rows: Sequence[dict[str, Any]],
) -> str:
    """Build a Mermaid graph for one metric/setting slice."""
    desc_label = DESC_TYPE_LABELS.get(description_type, description_type)
    mode_label = MODE_LABELS.get(mode, mode)
    title = f"{metric} - {desc_label} - {mode_label}"
    lines = [
        f"%% {metric}",
        "flowchart LR",
        f'  subgraph {_mermaid_node_id("title_" + metric + "_" + description_type + "_" + mode)}["{_mermaid_label(title)}"]',
        "    direction LR",
    ]
    node_labels: dict[str, str] = {}
    for row in rows:
        node_labels[row["model_a"]] = row["model_a_label"]
        node_labels[row["model_b"]] = row["model_b_label"]

    for agent_id, label in sorted(node_labels.items(), key=lambda item: item[1]):
        lines.append(f'    {_mermaid_node_id(agent_id)}["{_mermaid_label(label)}"]')

    significant_rows = [row for row in rows if row["is_significant"] and row["better_model"] and row["worse_model"]]
    for row in sorted(
        significant_rows,
        key=lambda item: (item["better_model_label"], item["worse_model_label"]),
    ):
        better_id = _mermaid_node_id(row["better_model"])
        worse_id = _mermaid_node_id(row["worse_model"])
        lines.append(f"    {better_id} --> {worse_id}")

    if not significant_rows:
        lines.append(
            f'    note_{_mermaid_node_id(metric + "_" + description_type + "_" + mode)}'
            f'["{_mermaid_label("No significant pairwise edges")}"]'
        )
    lines.append("  end")

    return "\n".join(lines)


def write_mermaid_files(report: dict[str, Any], report_dir: Path) -> list[Path]:
    """Write combined and per-setting Mermaid outputs."""
    written_paths: list[Path] = []
    combined_path = report_dir / REPORT_MERMAID_MD
    combined_path.write_text(render_mermaid_report(report), encoding="utf-8")
    written_paths.append(combined_path)

    mermaid_dir = report_dir / "mermaid"
    mermaid_dir.mkdir(parents=True, exist_ok=True)

    for metric in report["metadata"]["metrics"]:
        metric_rows = report["metrics"][metric]
        by_slice: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in metric_rows:
            by_slice.setdefault((row["description_type"], row["mode"]), []).append(row)

        combined_filename = f"{_slugify(metric)}__combined.mmd"
        combined_path = mermaid_dir / combined_filename
        combined_path.write_text(build_combined_mermaid_diagram(metric, by_slice) + "\n", encoding="utf-8")
        written_paths.append(combined_path)

        for description_type, mode in sort_type_mode_pairs(by_slice.keys()):
            filename = f"{_slugify(metric)}__{_slugify(description_type)}__{_slugify(mode)}.mmd"
            path = mermaid_dir / filename
            path.write_text(
                build_mermaid_diagram(metric, description_type, mode, by_slice[(description_type, mode)]) + "\n",
                encoding="utf-8",
            )
            written_paths.append(path)

    return written_paths


def _sorted_summary_agents(agent_ids: set[str]) -> list[str]:
    """Sort agents in the order used by benchmark result tables."""
    order = {agent_id: index for index, agent_id in enumerate(SUMMARY_AGENT_ORDER)}
    return sorted(agent_ids, key=lambda agent_id: (order.get(agent_id, len(order)), display_agent_name(agent_id) or agent_id))


def _setting_label(description_type: str, mode: str) -> str:
    """Format a description-type/mode setting for compact tables."""
    desc_label = DESC_TYPE_LABELS.get(description_type, description_type)
    mode_label = MODE_LABELS.get(mode, mode)
    return f"{desc_label} / {mode_label}"


def _format_n_pairs(n_pairs: Sequence[int]) -> str:
    """Format the shared-instance count for a table slice."""
    if not n_pairs:
        return "--"
    if len(n_pairs) == 1:
        return str(n_pairs[0])
    return f"{n_pairs[0]}-{n_pairs[-1]}"


def _oriented_summary_fields(row: dict[str, Any]) -> tuple[float, float, float, int, int, int]:
    """Orient effect size, CI, and win counts toward the reported better model."""
    if row["better_model"] == row["model_a"]:
        return (
            float(row["mean_difference"]),
            float(row["ci_low"]),
            float(row["ci_high"]),
            int(row["wins_a"]),
            int(row["ties"]),
            int(row["wins_b"]),
        )
    if row["better_model"] == row["model_b"]:
        return (
            float(-row["mean_difference"]),
            float(-row["ci_high"]),
            float(-row["ci_low"]),
            int(row["wins_b"]),
            int(row["ties"]),
            int(row["wins_a"]),
        )
    return (
        0.0,
        float(row["ci_low"]),
        float(row["ci_high"]),
        int(row["wins_a"]),
        int(row["ties"]),
        int(row["wins_b"]),
    )


def _mermaid_node_id(value: str) -> str:
    """Build a Mermaid-safe node identifier."""
    normalized = re.sub(r"[^a-zA-Z0-9_]+", "_", value).strip("_")
    if not normalized:
        normalized = "node"
    return f"node_{normalized}"


def _mermaid_label(value: str) -> str:
    """Escape a Mermaid quoted label."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _slugify(value: str) -> str:
    """Build a filesystem-safe slug."""
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    return normalized or "item"


def _latex_escape(value: str) -> str:
    """Escape a string for use in a LaTeX table cell."""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def _latex_summary_agent_label(agent_id: str) -> str:
    """Return a compact label for the LaTeX summary table."""
    return LATEX_SUMMARY_AGENT_LABELS.get(agent_id, display_agent_name(agent_id) or agent_id)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Paired significance analysis for benchmark model comparisons.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        action="append",
        dest="output_dirs",
        help="Benchmark output directory. Repeat to analyze multiple outputs. Default: auto-discover outputs/*/*.",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=DEFAULT_REPORT_DIR,
        help="Directory where JSON and Markdown reports are written.",
    )
    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path("./instances.csv"),
        help="Path to instances.csv.",
    )
    parser.add_argument(
        "--metric",
        action="append",
        dest="metrics",
        choices=list(DEFAULT_METRICS),
        help="Metric to analyze. Repeatable. Default: all supported metrics.",
    )
    parser.add_argument("--agent-id", action="append", dest="agent_ids", help="Optional agent filter. Repeatable.")
    parser.add_argument(
        "--description-type",
        action="append",
        dest="description_types",
        help="Optional description type filter. Repeatable.",
    )
    parser.add_argument("--mode", action="append", dest="modes", help="Optional mode filter. Repeatable.")
    parser.add_argument(
        "--successful-only",
        action="store_true",
        help="Only include evaluation results whose inference finish_reason is success.",
    )
    parser.add_argument("--alpha", type=float, default=DEFAULT_ALPHA, help="FDR threshold for significance.")
    parser.add_argument(
        "--permutations",
        type=int,
        default=DEFAULT_PERMUTATIONS,
        help="Monte Carlo sign-flip permutations when exact enumeration is disabled.",
    )
    parser.add_argument(
        "--bootstrap-resamples",
        type=int,
        default=DEFAULT_BOOTSTRAP_RESAMPLES,
        help="Bootstrap resamples for paired mean confidence intervals.",
    )
    parser.add_argument(
        "--exact-threshold",
        type=int,
        default=DEFAULT_EXACT_THRESHOLD,
        help="Use exact enumeration when the count of non-zero paired differences is at most this value.",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Random seed for Monte Carlo steps.")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    """Validate numeric CLI arguments before running analysis."""
    if not (0 < args.alpha <= 1):
        raise SystemExit("--alpha must be in (0, 1]")
    if args.permutations <= 0:
        raise SystemExit("--permutations must be positive")
    if args.bootstrap_resamples <= 0:
        raise SystemExit("--bootstrap-resamples must be positive")
    if args.exact_threshold < 0:
        raise SystemExit("--exact-threshold must be non-negative")


def main() -> None:
    args = parse_args()
    validate_args(args)
    output_dirs = [path.resolve() for path in args.output_dirs] if args.output_dirs else discover_output_dirs()
    if not output_dirs:
        raise SystemExit("No benchmark output directories found. Pass --output-dir explicitly.")

    report = build_report(
        output_dirs=output_dirs,
        instances_csv=args.instances_csv.resolve(),
        metrics=args.metrics or list(DEFAULT_METRICS),
        agent_ids=args.agent_ids,
        description_types=args.description_types,
        modes=args.modes,
        successful_only=args.successful_only,
        alpha=args.alpha,
        permutations=args.permutations,
        bootstrap_resamples=args.bootstrap_resamples,
        exact_threshold=args.exact_threshold,
        seed=args.seed,
    )

    report_dir_arg = args.report_dir
    report_dir = report_dir_arg.resolve()
    report_dir.mkdir(parents=True, exist_ok=True)

    json_path = report_dir / REPORT_JSON
    md_path = report_dir / REPORT_MD
    latex_summary_path = report_dir / REPORT_LATEX_SUMMARY
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_markdown_report(report), encoding="utf-8")
    latex_summary_path.write_text(render_latex_summary_table(report), encoding="utf-8")
    mermaid_paths = write_mermaid_files(report, report_dir)

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Wrote {latex_summary_path}")
    for path in mermaid_paths:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
