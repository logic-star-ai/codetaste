"""Statistics tables for analysis results."""

from collections import defaultdict

from refactoring_benchmark.analyze.models import (AgentDescriptionData,
                                                  AnalysisData,
                                                  format_type_mode_label,
                                                  sort_type_mode_pairs)
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
