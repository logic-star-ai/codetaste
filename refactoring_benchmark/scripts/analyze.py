"""CLI script to analyze evaluation results and generate plots by description type."""

import argparse
from pathlib import Path

from refactoring_benchmark.analyze.loader import (
    discover_output_dirs,
    load_all_results,
    organize_data,
    validate_analysis_data,
)
from refactoring_benchmark.analyze.metrics import ALL_METRICS
from refactoring_benchmark.analyze.plotting import create_plot, save_plot
from refactoring_benchmark.analyze.config import PlotConfig
from refactoring_benchmark.analyze.filters import filter_no_timeouts, filter_successful_only
from refactoring_benchmark.analyze.statistics import print_finish_reason_table, print_statistics_table
from refactoring_benchmark.utils.common import load_instances_from_csv


def main():
    """Analyze evaluation results and generate plots."""
    parser = argparse.ArgumentParser(
        description="Analyze evaluation results by description type",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default: auto-discover all 'output*' directories
  python -m refactoring_benchmark.scripts.analyze

  # Specify output directories
  python -m refactoring_benchmark.scripts.analyze --output-dir output --output-dir output_nano

  # Filter by agent
  python -m refactoring_benchmark.scripts.analyze --agent-id agent1 --agent-id agent2

  # Filter by description type
  python -m refactoring_benchmark.scripts.analyze --description-type standard --description-type minimal

  # Generate specific metrics with bar chart
  python -m refactoring_benchmark.scripts.analyze --metric ifr --plot-type bar

  # Use median aggregation
  python -m refactoring_benchmark.scripts.analyze --aggregation median

  # Only successful inference runs
  python -m refactoring_benchmark.scripts.analyze --successful-only

  # Plot precision metrics (requires null agent)
  python -m refactoring_benchmark.scripts.analyze --metric precision_overall

  # Custom instances CSV
  python -m refactoring_benchmark.scripts.analyze --instances-csv ./custom_instances.csv
        """,
    )
    # Output directory arguments
    parser.add_argument(
        "--output-dir",
        type=Path,
        action="append",
        dest="output_dirs",
        help="Output directory containing evaluation results (can be specified multiple times). "
        "Default: auto-discover all directories starting with 'output' in current directory.",
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
            print("Error: No directories starting with 'output' found in current directory")
            print("Hint: Use --output-dir to specify directories manually")
            return
        print(f"Auto-discovered {len(output_dirs)} output directories:")
        for d in output_dirs:
            print(f"  - {d}")

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
    print(f"Scanning {len(output_dirs)} output director{'y' if len(output_dirs) == 1 else 'ies'} for evaluation results...")
    results = load_all_results(output_dirs, instances, agent_ids=args.agent_ids)
    print(f"Found {len(results)} evaluation results")

    if not results:
        print("No evaluation results found")
        return

    # Prepare filters
    default_filters = [filter_no_timeouts()]
    print("Applying default filter: Exclude timed-out inference runs (finish_reason='timeout')")
    filters = default_filters + []
    if args.successful_only:
        filters.append(filter_successful_only())
        print("Filtering: Only successful inference runs (finish_reason='success')")

    # Create plot configuration
    plot_config = PlotConfig(show_error_bars=not args.no_error_bars)

    # Print finish_reason statistics if requested
    if args.statistics:
        filtered_results = results[:]
        if args.agent_ids:
            filtered_results = [r for r in filtered_results if r.agent_config.id in args.agent_ids]
        if args.description_types:
            filtered_results = [
                r for r in filtered_results
                if r.inference_metadata and r.inference_metadata.description_type in args.description_types
            ]
        print_finish_reason_table(filtered_results, "Filtered by Description Type and Agent ID")

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

        # Validate data
        try:
            validate_analysis_data(data, args.agent_ids, args.description_types)
        except ValueError as e:
            print(f"  Error: {e}")
            return

        # Print summary
        print(f"  Found {len(data.get_agent_ids())} agents: {', '.join(data.get_agent_ids())}")
        print(f"  Found {len(data.get_description_types())} description types: {', '.join(data.get_description_types())}")

        # Generate plot
        print(f"  Generating {args.plot_type} plot with {args.aggregation} aggregation...")
        try:
            fig = create_plot(
                data,
                metric_name,
                plot_type=args.plot_type,
                aggregation=args.aggregation,
                config=plot_config if metric_name != "cost" else PlotConfig(show_error_bars=False, ylim_max=10)
            )

            # Print statistics table if requested
            if args.statistics:
                print_statistics_table(data, metric_name, args.aggregation)

            # Save plot
            output_filename = f"{metric_name}_{args.plot_type}_{args.aggregation}.png"
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
