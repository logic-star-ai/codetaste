"""Statistics tables for analysis results."""

from collections import defaultdict

from refactoring_benchmark.analyze.models import (
    AgentDescriptionData,
    AnalysisData,
    format_type_mode_label,
    sort_type_mode_pairs,
)
from refactoring_benchmark.evaluation.models import EvaluationResult


def print_statistics_table(data: AnalysisData, metric_name: str, aggregation: str) -> None:
    """Print comparison table with agent statistics, including count, mean, and CI."""
    agents = data.get_agent_ids()
    type_mode_pairs = data.get_type_mode_pairs()

    if not agents or not type_mode_pairs:
        return

    print(f"\n  Statistics for {metric_name.upper()} ({aggregation}):")
    print("  " + "=" * 115)
    # Updated Header: Added Metric Count
    print(f"  {'Agent / Description Type / Mode':<50} {'Metric Count':<15} {'Metric Mean':<15} {'Metric CI':<30}")
    print("  " + "-" * 115)

    for agent_id in agents:
        all_metrics = []
        individual_results = []

        for desc_type, mode in type_mode_pairs:
            agent_desc_data = data.get_data(agent_id, desc_type, mode)
            if agent_desc_data:
                all_metrics.extend(agent_desc_data.metric_values)
                individual_results.append(agent_desc_data)

        if all_metrics:
            combined_data = AgentDescriptionData(
                agent_id=agent_id, description_type="COMBINED", mode="combined", metric_values=all_metrics
            )

            # 1. Updated Combined Row: Added combined_data.count
            if aggregation == "mean":
                ci_low, ci_high = combined_data.confidence_interval()
                print(
                    f"  {agent_id:<50} {combined_data.count:<15} {combined_data.mean:<15.4f} [{ci_low:.4f}, {ci_high:.4f}]"
                )
            else:  # median
                print(f"  {agent_id:<50} {combined_data.count:<15} {combined_data.median:<15.4f} {'N/A (median)':<30}")

            # 2. Updated Individual Breakdown Rows: Added desc_data.count
            for desc_data in individual_results:
                label = f"   └─ {format_type_mode_label(desc_data.description_type, desc_data.mode, separator='/')}"
                if aggregation == "mean":
                    ci_low, ci_high = desc_data.confidence_interval()
                    print(f"  {label:<50} {desc_data.count:<15} {desc_data.mean:<15.4f} [{ci_low:.4f}, {ci_high:.4f}]")
                else:
                    print(f"  {label:<50} {desc_data.count:<15} {desc_data.median:<15.4f} {'N/A (median)':<30}")

            print("  " + "." * 115)
    print("  " + "=" * 115)


def print_finish_reason_table(results: list[EvaluationResult], filter_desc: str = "") -> None:
    """Print finish_reason counts grouped by agent, description type, and mode.

    Args:
        results: List of evaluation results
        filter_desc: Description of applied filters for the title
    """
    # Group results by (agent_id, description_type, mode) and count finish_reasons
    counts = defaultdict(lambda: defaultdict(int))

    for result in results:
        if (
            not result.inference_metadata
            or not result.inference_metadata.description_type
            or not result.inference_metadata.mode
        ):
            continue
        agent_id = result.agent_config.id
        desc_type = result.inference_metadata.description_type
        mode = result.inference_metadata.mode
        finish_reason = result.inference_metadata.finish_reason
        counts[(agent_id, desc_type, mode)][finish_reason] += 1

    if not counts:
        return

    # Discover all unique finish_reasons and agents
    all_finish_reasons = sorted(set(reason for count_dict in counts.values() for reason in count_dict.keys()))
    agents = sorted(set(k[0] for k in counts.keys()))
    type_mode_pairs = sort_type_mode_pairs((k[1], k[2]) for k in counts.keys())

    # Calculate column widths
    agent_col_width = 55
    reason_col_width = max(20, max(len(r) for r in all_finish_reasons) + 2)
    total_col_width = 10

    # Print header
    title = "\n  Finish Reason Statistics"
    if filter_desc:
        title += f" ({filter_desc})"
    print(title + ":")

    header_width = agent_col_width + len(all_finish_reasons) * reason_col_width + total_col_width
    print("  " + "=" * header_width)
    # Column headers
    header = f"  {'Agent / Description Type / Mode':<{agent_col_width}}"
    for reason in all_finish_reasons:
        header += f"{reason:>{reason_col_width}}"
    header += f"{'TOTAL':>{total_col_width}}"
    print(header)
    print("  " + "-" * header_width)

    # Print data grouped by agent
    for agent_id in agents:
        # Collect data for this agent across all description types
        agent_totals = defaultdict(int)
        agent_desc_data = []

        for desc_type, mode in type_mode_pairs:
            key = (agent_id, desc_type, mode)
            if key in counts:
                agent_desc_data.append((desc_type, mode, counts[key]))
                for reason, count in counts[key].items():
                    agent_totals[reason] += count

        if not agent_desc_data:
            continue

        # Print combined row for agent
        row = f"  {agent_id:<{agent_col_width}}"
        for reason in all_finish_reasons:
            row += f"{agent_totals.get(reason, 0):>{reason_col_width}}"
        total = sum(agent_totals.values())
        row += f"{total:>{total_col_width}}"
        print(row)

        # Print breakdown by description type
        for desc_type, mode, desc_counts in agent_desc_data:
            label = f"   └─ {format_type_mode_label(desc_type, mode, separator='/')}"
            row = f"  {label:<{agent_col_width}}"
            for reason in all_finish_reasons:
                row += f"{desc_counts.get(reason, 0):>{reason_col_width}}"
            total = sum(desc_counts.values())
            row += f"{total:>{total_col_width}}"
            print(row)

        print("  " + "." * header_width)

    print("  " + "=" * header_width)


LATEX_AGENT_NAME_MAPPING = {
    "codex-v0.77.0-gpt-5.2": "GPT-5.2",
    "codex-v0.77.0-gpt-5.1-codex-mini": "GPT-5.1 Codex Mini",
    "claude-code-v2.0.76-sonnet45": "Claude Sonnet 4.5",
    "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct": "Qwen3",
    "golden_agent": "Golden Patch",
    "null_agent": "Base Commit",
}
LATEX_DESC_TYPE_LABELS = {
    "open": "Open",
    "instructed": "Instructed",
}
LATEX_MODE_LABELS = {
    "direct": "Direct",
    "plan": "Plan",
    "multiplan": "Multiplan",
}
LATEX_SUMMARY_ONLY_AGENTS = {"golden_agent", "null_agent"}


def _combine_agent_data(data: AnalysisData, agent_id: str) -> AgentDescriptionData | None:
    all_metrics = []
    for (agent, _desc_type, _mode), agent_desc_data in data.data.items():
        if agent == agent_id:
            all_metrics.extend(agent_desc_data.metric_values)
    if not all_metrics:
        return None
    return AgentDescriptionData(
        agent_id=agent_id,
        description_type="COMBINED",
        mode="combined",
        metric_values=all_metrics,
    )


def _sorted_agent_ids(agent_ids: set[str]) -> list[str]:
    agent_order = {
        "codex-v0.77.0-gpt-5.2": 0,
        "codex-v0.77.0-gpt-5.1-codex-mini": 1,
        "claude-code-v2.0.76-sonnet45": 2,
        "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct": 3,
        "golden_agent": 4,
        "null_agent": 5,
    }
    return sorted(agent_ids, key=lambda x: agent_order.get(x, 999))


def _format_metric_cell(
    data: AgentDescriptionData | None, *, bold: bool = False, include_ci: bool = True
) -> str:
    if data is None or data.count == 0:
        return "--"
    mean = data.mean * 100
    mean_str = f"{mean:.1f}"
    if bold:
        mean_str = f"\\textbf{{{mean_str}}}"
    if not include_ci:
        return mean_str
    ci_low, ci_high = data.confidence_interval()
    return f"{mean_str} {{\\tiny [{ci_low * 100:.1f}, {ci_high * 100:.1f}]}}"


def _format_desc_label(desc_type: str) -> str:
    return LATEX_DESC_TYPE_LABELS.get(desc_type, desc_type.replace("_", " ").title())


def _format_mode_label(mode: str) -> str:
    return LATEX_MODE_LABELS.get(mode, mode.replace("_", " ").title())


LATEX_METRIC_LABELS = {
    "f1": r"F$_1$",
    "ifr": r"\textsc{Ifr}",
    "ifr_x_test_success": r"$\mathcal{A}$",
    "ifr_added_x_test_success": r"$\mathcal{A}^{+}$",
    "ifr_removed_x_test_success": r"$\mathcal{A}^{-}$",
    "strict_ifr_x_test_success": r"Strict",
    "ifr_added": r"\textsc{Ifr}$^{+}$",
    "ifr_removed": r"\textsc{Ifr}$^{-}$",
    "test_success": r"\textsc{Pass}",
    "precision_added": r"\textsc{Prec}$^{+}$",
    "precision_removed": r"\textsc{Prec}$^{-}$",
    "precision_overall": r"\textsc{Prec}",
}

LATEX_TABLE_EXCLUDED_METRICS = {"diff_added_lines", "diff_removed_lines", "diff_delta_lines", "cost"}


def _default_metrics() -> list[str]:
    from refactoring_benchmark.analyze.metrics import ALL_METRICS

    return [m for m in ALL_METRICS if m not in LATEX_TABLE_EXCLUDED_METRICS]


def get_table_metrics() -> list[str]:
    """Return ordered metrics suitable for the wide LaTeX table."""
    return _default_metrics()


def _format_metric_header(metric_name: str) -> str:
    label = LATEX_METRIC_LABELS.get(metric_name, metric_name.replace("_", " ").title())
    return f"{label} (\\%) [CI]"


def build_latex_metrics_table(
    metric_data_map: dict[str, AnalysisData],
    metrics: list[str] | None = None,
    agent_ids: list[str] | None = None,
    caption: str | None = None,
    label: str | None = None,
) -> str:
    """Build a wide LaTeX table for metrics with 95% CIs (percentages)."""
    if not metric_data_map:
        return ""

    metrics = metrics or _default_metrics()
    metrics = [m for m in metrics if m in metric_data_map]
    if not metrics:
        return ""

    # Derive ordering from available data
    all_agents = set()
    all_pairs = set()
    for data in metric_data_map.values():
        all_agents.update(data.get_agent_ids())
        all_pairs.update(data.get_type_mode_pairs())

    if not all_agents or not all_pairs:
        return ""

    agents = _sorted_agent_ids(all_agents)
    if agent_ids:
        agents = [agent for agent in agents if agent in agent_ids]
    if not agents:
        return ""

    type_mode_pairs = sort_type_mode_pairs(all_pairs)
    desc_to_modes: dict[str, list[str]] = {}
    for desc_type, mode in type_mode_pairs:
        desc_to_modes.setdefault(desc_type, []).append(mode)

    column_spec = "l" + "c" * (1 + len(metrics))
    header_cells = " & ".join(_format_metric_header(metric) for metric in metrics)

    if caption is None:
        caption = "Full experimental results across all tracks, models, and metrics in percents with 95 \\% confidence intervals."
    if label is None:
        label = "tab:full-metric-results-wide"

    lines = [
        r"\begin{table}[p]",
        rf"  \caption{{{caption}}}",
        rf"  \label{{{label}}}",
        r"  \begin{center}",
        r"    \begin{small}",
        r"    \resizebox{\textwidth}{!}{%",
        rf"        \begin{{tabular}}{{{column_spec}}}",
        r"          \toprule",
        rf"           & {{}} & {header_cells} \\",
        r"          \midrule",
    ]

    for agent_id in agents:
        agent_label = LATEX_AGENT_NAME_MAPPING.get(agent_id, agent_id)
        combined_cells = []
        for metric in metrics:
            combined_data = _combine_agent_data(metric_data_map.get(metric, AnalysisData()), agent_id)
            combined_cells.append(_format_metric_cell(combined_data, bold=True, include_ci=False))

        lines.append(f"          \\textbf{{{agent_label}}} & {{}} & " + " & ".join(combined_cells) + r" \\")

        if agent_id in LATEX_SUMMARY_ONLY_AGENTS:
            lines.append(r"          \midrule")
            continue

        for desc_type, modes in desc_to_modes.items():
            desc_label = _format_desc_label(desc_type)
            if len(modes) == 1:
                mode = modes[0]
                row_label = rf"\hspace{{1em}} $\llcorner$ {desc_label}"
                row_cells = []
                for metric in metrics:
                    data = metric_data_map.get(metric)
                    desc_data = data.get_data(agent_id, desc_type, mode) if data else None
                    row_cells.append(
                        _format_metric_cell(desc_data, include_ci=agent_id not in LATEX_SUMMARY_ONLY_AGENTS)
                    )
                lines.append(f"          {row_label} & {{}} & " + " & ".join(row_cells) + r" \\")
            else:
                for mode in modes:
                    row_label = rf"\hspace{{1em}} $\llcorner$ {desc_label}"
                    mode_label = _format_mode_label(mode)
                    row_cells = []
                    for metric in metrics:
                        data = metric_data_map.get(metric)
                        desc_data = data.get_data(agent_id, desc_type, mode) if data else None
                        row_cells.append(
                            _format_metric_cell(desc_data, include_ci=agent_id not in LATEX_SUMMARY_ONLY_AGENTS)
                        )
                    lines.append(f"          {row_label} & {mode_label} & " + " & ".join(row_cells) + r" \\")

        lines.append(r"          \midrule")

    if lines[-1] == r"          \midrule":
        lines.pop()

    lines.extend(
        [
            r"          \bottomrule",
            r"        \end{tabular}}",
            r"    \end{small}",
            r"  \end{center}",
            r"  \vskip -0.1in",
            r"\end{table}",
        ]
    )

    return "\n".join(lines)
