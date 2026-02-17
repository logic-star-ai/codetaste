"""CLI script to analyze evaluation results and generate plots by description type and mode."""

import argparse
from pathlib import Path

from refactoring_benchmark.analyze.config import PlotConfig
from refactoring_benchmark.analyze.filters import filter_results, filter_successful_only
from refactoring_benchmark.analyze.loader import (
    discover_output_dirs,
    load_all_results,
    organize_data,
    validate_analysis_data,
)
from refactoring_benchmark.analyze.metrics import ALL_METRICS
from refactoring_benchmark.analyze.plotting import create_plot, save_plot
from refactoring_benchmark.analyze.statistics import (
    build_latex_metrics_table,
    print_finish_reason_table,
    print_statistics_table,
)
from refactoring_benchmark.utils.common import load_instances_from_csv


def main():
    """Analyze evaluation results and generate plots."""
    parser = argparse.ArgumentParser(
        description="Analyze evaluation results by description type and mode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default: auto-discover all outputs/*/* directories
  python -m refactoring_benchmark.cli.analyze

  # Specify output directories
  python -m refactoring_benchmark.cli.analyze --output-dir outputs/instructed/direct --output-dir outputs/open/direct

  # Filter by agent
  python -m refactoring_benchmark.cli.analyze --agent-id agent1 --agent-id agent2

  # Filter by description type
  python -m refactoring_benchmark.cli.analyze --description-type instructed --description-type open

  # Filter by mode
  python -m refactoring_benchmark.cli.analyze --mode direct --mode plan

  # Generate specific metrics with bar chart
  python -m refactoring_benchmark.cli.analyze --metric ifr --plot-type bar

  # Use median aggregation
  python -m refactoring_benchmark.cli.analyze --aggregation median

  # Only successful inference runs
  python -m refactoring_benchmark.cli.analyze --successful-only

  # Plot precision metrics (requires null agent)
  python -m refactoring_benchmark.cli.analyze --metric precision_overall

  # Custom instances CSV
  python -m refactoring_benchmark.cli.analyze --instances-csv ./custom_instances.csv
        """,
    )
    # Output directory arguments
    parser.add_argument(
        "--output-dir",
        type=Path,
        action="append",
        dest="output_dirs",
        help="Output directory containing evaluation results (can be specified multiple times). "
        "Default: auto-discover all directories under ./outputs/<description_type>/<mode>.",
    )

    # Filtering arguments
    parser.add_argument(
        "--agent-id",
        action="append",
        dest="agent_ids",
        help="Filter by agent ID (can be specified multiple times). Default: all agents found in data.",
    )
    parser.add_argument(
        "--description-type",
        action="append",
        dest="description_types",
        help="Filter by description type (can be specified multiple times). "
        "Default: all description types found in data.",
    )
    parser.add_argument(
        "--mode",
        action="append",
        dest="modes",
        help="Filter by inference mode (direct, plan, multiplan). " "Default: all modes found in data.",
    )
    parser.add_argument(
        "--successful-only",
        action="store_true",
        help="Only include inference runs with finish_reason='success'",
    )

    # Metric arguments
    parser.add_argument(
        "--metric",
        action="append",
        dest="metrics",
        choices=ALL_METRICS,
        help=f"Metrics to plot (can be specified multiple times). "
        f"Default: ifr, test_success (precision metrics require null agent). "
        f"Available: {', '.join(ALL_METRICS)}",
    )

    # Plot arguments
    parser.add_argument(
        "--plot-type",
        type=str,
        default="line",
        choices=["line", "bar", "scatter"],
        help="Type of plot to generate (default: line)",
    )
    parser.add_argument(
        "--aggregation",
        type=str,
        default="mean",
        choices=["mean", "median"],
        help="How to aggregate metric values (default: mean)",
    )
    parser.add_argument(
        "--no-error-bars",
        action="store_true",
        help="Disable 95 percent confidence interval error bars",
    )
    parser.add_argument(
        "--no-ylabel",
        action="store_true",
        help="Hide y-axis label",
    )
    parser.add_argument(
        "--no-legend",
        action="store_true",
        help="Hide legend",
    )
    parser.add_argument(
        "--legend-position",
        type=str,
        default="upper_left",
        choices=["upper_left", "upper_right", "lower_left"],
        help="Legend position (upper_left, upper_right, lower_left). Default: upper_left",
    )
    parser.add_argument(
        "--ytick-step",
        type=int,
        default=None,
        help="Y-axis tick step in percent (default: 5)",
    )

    # Other arguments
    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path("./instances.csv"),
        help="Path to instances.csv file (default: ./instances.csv)",
    )
    parser.add_argument(
        "--plots-dir",
        type=Path,
        default=Path("./analyze"),
        help="Directory to save plots (default: ./analyze)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution for saved plots (default: 300)",
    )
    parser.add_argument(
        "--statistics",
        action="store_true",
        help="Print comparison table with mean and confidence interval statistics",
    )

    args = parser.parse_args()

    # Determine output directories
    if args.output_dirs:
        output_dirs = [d.resolve() for d in args.output_dirs]
        for output_dir in output_dirs:
            if not output_dir.exists():
                print(f"Error: Output directory {output_dir} does not exist")
                return
    else:
        # Auto-discover
        output_dirs = discover_output_dirs()
        if not output_dirs:
            print("Error: No directories found under ./outputs/<description_type>/<mode>")
            print("Hint: Use --output-dir to specify directories manually")
            return
        print(f"Auto-discovered {len(output_dirs)} output directories:")
        for d in output_dirs:
            print(f"  - {d}")

    # Include pseudo agent outputs when explicitly requested
    if args.agent_ids and any(agent in {"golden_agent", "null_agent"} for agent in args.agent_ids):
        pseudo_agents_dir = Path("./outputs/pseudo_agents/direct").resolve()
        if pseudo_agents_dir.exists() and pseudo_agents_dir not in output_dirs:
            output_dirs.append(pseudo_agents_dir)
            print(f"Added pseudo agent output directory: {pseudo_agents_dir}")

    # Load instances from CSV
    instances_csv = args.instances_csv.resolve()
    if not instances_csv.exists():
        print(f"Error: instances.csv not found at {instances_csv}")
        return

    try:
        instances = load_instances_from_csv(instances_csv)
        print(f"Loaded {len(instances)} instances from {instances_csv.name}")
    except Exception as e:
        print(f"Error: Failed to load instances from CSV: {e}")
        return

    if not instances:
        print("Error: No instances found in CSV")
        return

    # Determine metrics to plot (default: non-precision metrics only)
    if args.metrics:
        metrics_to_plot = args.metrics
    else:
        # Default: ifr and test_success (not precision metrics by default since they require null agent)
        metrics_to_plot = ["ifr", "test_success"]
    print(f"Metrics to plot: {', '.join(metrics_to_plot)}")

    # Load evaluation results
    print(
        f"Scanning {len(output_dirs)} output director{'y' if len(output_dirs) == 1 else 'ies'} for evaluation results..."
    )
    results = load_all_results(output_dirs, instances, agent_ids=args.agent_ids)
    print(f"Found {len(results)} evaluation results")

    if not results:
        print("No evaluation results found")
        return

    # Prepare filters
    filters = []
    if args.successful_only:
        filters.append(filter_successful_only())
        print("Filtering: Only successful inference runs (finish_reason='success')")

    # Create plot configuration
    plot_config_kwargs = dict(
        show_error_bars=not args.no_error_bars,
        show_ylabel=not args.no_ylabel,
        show_legend=not args.no_legend,
        legend_position=args.legend_position,
    )
    if args.ytick_step is not None:
        plot_config_kwargs["ytick_step"] = args.ytick_step
    plot_config = PlotConfig(**plot_config_kwargs)

    # Print finish_reason statistics if requested
    if args.statistics:
        filtered_results = filter_results(
            results,
            agent_ids=args.agent_ids,
            description_types=args.description_types,
            modes=args.modes,
        )
        print_finish_reason_table(filtered_results, "Filtered by Description Type, Mode, and Agent ID")

    # Generate LaTeX table for the requested metrics and agents
    try:
        latex_metrics_data = {}
        for metric in metrics_to_plot:
            metric_data = organize_data(results, metric, filters=filters if filters else None)
            if args.agent_ids:
                metric_data = metric_data.filter_agents(args.agent_ids)
            if args.description_types:
                metric_data = metric_data.filter_description_types(args.description_types)
            if args.modes:
                metric_data = metric_data.filter_modes(args.modes)
            latex_metrics_data[metric] = metric_data

        caption = "Results for selected metrics and agents in percents with 95 \\% confidence intervals."
        label = "tab:metric-results"

        latex_table = build_latex_metrics_table(
            latex_metrics_data,
            metrics=metrics_to_plot,
            agent_ids=args.agent_ids,
            caption=caption,
            label=label,
        )
        if latex_table:
            args.plots_dir.mkdir(parents=True, exist_ok=True)
            latex_path = args.plots_dir / "metric_results.tex"
            latex_path.write_text(latex_table)
            print(f"Saved LaTeX table to {latex_path}")
    except Exception as e:
        print(f"Warning: Failed to generate LaTeX table: {e}")

    # Process each metric
    for metric_name in metrics_to_plot:
        print(f"\nProcessing metric: {metric_name}")

        # Organize data for this metric
        print("  Organizing data...")
        try:
            data = organize_data(results, metric_name, filters=filters if filters else None)
        except ValueError as e:
            print(f"  Error: {e}")
            continue

        # Apply agent and description type filters
        if args.agent_ids:
            data = data.filter_agents(args.agent_ids)
        if args.description_types:
            data = data.filter_description_types(args.description_types)
        if args.modes:
            data = data.filter_modes(args.modes)

        # Validate data
        try:
            validate_analysis_data(data, args.agent_ids, args.description_types, args.modes)
        except ValueError as e:
            print(f"  Error: {e}")
            return

        # Print summary
        print(f"  Found {len(data.get_agent_ids())} agents: {', '.join(data.get_agent_ids())}")
        type_mode_pairs, type_mode_labels = data.get_type_mode_pairs_with_labels(separator="/")
        print(f"  Found {len(type_mode_pairs)} description type/mode pairs: {', '.join(type_mode_labels)}")

        # Generate plot
        print(f"  Generating {args.plot_type} plot with {args.aggregation} aggregation...")
        try:
            if len(output_dirs) != 1:
                max_mean = max([v.mean for k, v in data.data.items()])
                max_ci = max([v.confidence_interval()[1] - v.mean for k, v in data.data.items()])
                print(f"    Setting y-axis limit to {max_mean:.4f} for better visibility")
                y_lim_min = 0
                y_lim_max = max_mean + 1 * max_ci + 0.01
                ytick_step = 5
                while (y_lim_max - y_lim_min) * 100 / ytick_step > 15:
                    ytick_step += 5
                config = plot_config.model_copy(
                    update={"ylim_max": y_lim_max, "ylim_min": y_lim_min, "ytick_step": ytick_step}
                )
            else:
                config = plot_config
            fig = create_plot(data, metric_name, plot_type=args.plot_type, aggregation=args.aggregation, config=config)

            # Print statistics table if requested
            if args.statistics:
                print_statistics_table(data, metric_name, args.aggregation)

            # Save plot
            output_filename = f"{metric_name}_{args.plot_type}_{args.aggregation}.pdf"
            output_path = args.plots_dir / output_filename
            save_plot(fig, output_path, dpi=args.dpi)
            print(f"  Saved plot to {output_path}")

        except Exception as e:
            print(f"  Error generating plot: {e}")
            import traceback

            traceback.print_exc()

    print("\nDone!")


if __name__ == "__main__":
    main()
