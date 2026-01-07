"""CLI script to generate IFR plots from evaluation results."""

import argparse
from pathlib import Path
from refactoring_benchmark.analyze import (
    load_all_results,
    organize_data,
    create_ifr_plots,
    filter_has_execution_environment,
    filter_successful_only,
    compute_all_agent_statistics,
)


def print_statistics_summary(all_stats):
    """Print formatted statistics summary."""
    combination_names = {
        1: "All instances + All validity statuses",
        2: "All instances + Valid tests only",
        3: "All instances + Invalid tests only",
        4: "IFR > 0 + All validity statuses",
        5: "IFR > 0 + Valid tests only",
        6: "IFR > 0 + Invalid tests only",
    }

    for combo_id in range(1, 7):
        combo_stats = all_stats.combinations[combo_id]
        print(f"\n{'='*80}")
        print(f"Combination {combo_id}: {combination_names[combo_id]}")
        print(f"{'='*80}")

        # Print header
        print(f"\n{'Agent':<40} {'Metric':<15} {'Mean':>10} {'Median':>10} {'Count':>8}")
        print("-" * 80)

        # Print statistics for each agent
        for agent_id in sorted(combo_stats.agents.keys()):
            agent_stats = combo_stats.agents[agent_id]

            # Print Total IFR
            print(
                f"{agent_id:<40} {'Total IFR':<15} "
                f"{agent_stats.total_ifr.mean:>10.2f} "
                f"{agent_stats.total_ifr.median:>10.2f} "
                f"{agent_stats.total_ifr.count:>8d}"
            )

            # Print Positive IFR
            print(
                f"{'':40} {'Positive IFR':<15} "
                f"{agent_stats.positive_ifr.mean:>10.2f} "
                f"{agent_stats.positive_ifr.median:>10.2f} "
                f"{agent_stats.positive_ifr.count:>8d}"
            )

            # Print Negative IFR
            print(
                f"{'':40} {'Negative IFR':<15} "
                f"{agent_stats.negative_ifr.mean:>10.2f} "
                f"{agent_stats.negative_ifr.median:>10.2f} "
                f"{agent_stats.negative_ifr.count:>8d}"
            )

            print("-" * 80)


def main():
    """Generate all IFR plots."""
    parser = argparse.ArgumentParser(
        description="Generate IFR plots from evaluation results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default: only instances with execution environment
  python -m refactoring_benchmark.scripts.analyze

  # Include all instances (even without execution environment)
  python -m refactoring_benchmark.scripts.analyze --include-no-exec-env

  # Only include successful inference runs
  python -m refactoring_benchmark.scripts.analyze --successful-only

  # Compute and print statistics summary
  python -m refactoring_benchmark.scripts.analyze --statistics

  # Combine filters: successful runs with statistics
  python -m refactoring_benchmark.scripts.analyze --successful-only --statistics

  # Use custom output directory
  python -m refactoring_benchmark.scripts.analyze --output-dir ./custom/output
        """
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./output"),
        help="Directory containing evaluation results (default: ./output)"
    )
    parser.add_argument(
        "--include-no-exec-env",
        action="store_true",
        help="Include instances without execution environment (default: False)"
    )
    parser.add_argument(
        "--statistics",
        action="store_true",
        help="Compute and print statistics summary for all agents"
    )
    parser.add_argument(
        "--successful-only",
        action="store_true",
        help="Only include inference runs with finish_reason='success'"
    )
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    if not output_dir.exists():
        print(f"Error: Output directory {output_dir} does not exist")
        return

    print(f"Scanning {output_dir} for evaluation results...")
    results = load_all_results(output_dir)
    print(f"Found {len(results)} evaluation results")

    if not results:
        print("No evaluation results found")
        return

    filters = []
    if not args.include_no_exec_env:
        filters.append(filter_has_execution_environment(True))
        print("Filtering: Only instances with execution environment")

    if args.successful_only:
        filters.append(filter_successful_only())
        print("Filtering: Only successful inference runs (finish_reason='success')")

    print("Organizing data...")
    data = organize_data(results, filters=filters if filters else None)
    print(f"Found {len(data.instances)} unique instances")

    if len(data.instances) == 0:
        print("No instances to plot after filtering")
        return

    # Compute and print statistics if requested
    if args.statistics:
        print("\nComputing statistics...")
        all_stats = compute_all_agent_statistics(data)
        print_statistics_summary(all_stats)
        print("\n")  # Extra newline before plotting section

    plots_dir = Path("./analyze")

    print("Generating plots...")
    create_ifr_plots(data, plots_dir)

    print("Done!")


if __name__ == "__main__":
    main()
