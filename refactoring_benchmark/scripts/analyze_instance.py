"""CLI script to analyze and plot metrics for each instance across agents."""

import argparse
from pathlib import Path

from refactoring_benchmark.analyze_instance.instance_analysis import (
    organize_instance_data,
    create_instance_plot,
    save_instance_plot,
)
from refactoring_benchmark.analyze.loader import discover_output_dirs, load_all_results
from refactoring_benchmark.analyze.metrics import ALL_METRICS
from refactoring_benchmark.analyze.config import PlotConfig
from refactoring_benchmark.analyze.filters import filter_successful_only
from refactoring_benchmark.utils.common import load_instances_from_csv


def main():
    """Analyze evaluation results and generate per-instance plots."""
    parser = argparse.ArgumentParser(
        description="Analyze and plot metrics for each instance across agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default: auto-discover all 'output*' directories
  python -m refactoring_benchmark.scripts.analyze_instance

  # Specify output directories
  python -m refactoring_benchmark.scripts.analyze_instance --output-dir output --output-dir output_abstract

  # Filter by agent
  python -m refactoring_benchmark.scripts.analyze_instance --agent-id agent1 --agent-id agent2

  # Generate specific metrics with heatmap
  python -m refactoring_benchmark.scripts.analyze_instance --metric ifr --plot-type heatmap

  # Only successful inference runs
  python -m refactoring_benchmark.scripts.analyze_instance --successful-only

  # Limit number of instances displayed
  python -m refactoring_benchmark.scripts.analyze_instance --max-instances 20

  # Plot multiple metrics
  python -m refactoring_benchmark.scripts.analyze_instance --metric ifr --metric test_success

  # Custom instances CSV
  python -m refactoring_benchmark.scripts.analyze_instance --instances-csv ./custom_instances.csv
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
        "--successful-only",
        action="store_true",
        help="Only include inference runs with finish_reason='success'",
    )
    parser.add_argument(
        "--max-instances",
        type=int,
        help="Maximum number of instances to display in plots (default: all instances)",
    )

    # Metric arguments
    parser.add_argument(
        "--metric",
        action="append",
        dest="metrics",
        choices=ALL_METRICS,
        help=f"Metrics to plot (can be specified multiple times). "
        f"Default: ifr, test_success. "
        f"Available: {', '.join(ALL_METRICS)}",
    )

    # Plot arguments
    parser.add_argument(
        "--plot-type",
        type=str,
        default="heatmap",
        choices=["line", "bar", "heatmap"],
        help="Type of plot to generate (default: heatmap)",
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
        default=Path("./analyze_instance"),
        help="Directory to save plots (default: ./analyze_instance)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution for saved plots (default: 300)",
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

    # Determine metrics to plot (default: ifr and test_success)
    if args.metrics:
        metrics_to_plot = args.metrics
    else:
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
    plot_config = PlotConfig()

    # Process each metric
    for metric_name in metrics_to_plot:
        print(f"\nProcessing metric: {metric_name}")

        # Organize data for this metric
        print("  Organizing data...")
        try:
            data = organize_instance_data(results, metric_name, filters=filters if filters else None)
        except ValueError as e:
            print(f"  Error: {e}")
            continue

        # Apply agent filter
        if args.agent_ids:
            data = data.filter_agents(args.agent_ids)

        # Check if we have data
        instance_keys = data.get_instance_keys()
        agent_ids = data.get_agent_ids()

        if not instance_keys:
            print(f"  No instances with {metric_name} data found")
            continue

        if not agent_ids:
            print(f"  No agents with {metric_name} data found")
            continue

        # Print summary
        print(f"  Found {len(instance_keys)} instances")
        print(f"  Found {len(agent_ids)} agents: {', '.join(agent_ids)}")

        # Generate plot
        print(f"  Generating {args.plot_type} plot...")
        try:
            fig = create_instance_plot(
                data,
                metric_name,
                plot_type=args.plot_type,
                config=plot_config,
                max_instances=args.max_instances,
            )

            # Save plot
            output_filename = f"{metric_name}_{args.plot_type}.pdf"
            output_path = args.plots_dir / output_filename
            save_instance_plot(fig, output_path, dpi=args.dpi)
            print(f"  Saved plot to {output_path}")

        except Exception as e:
            print(f"  Error generating plot: {e}")
            import traceback

            traceback.print_exc()

    print("\nDone!")


if __name__ == "__main__":
    main()
