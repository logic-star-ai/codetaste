"""CLI script to analyze pass-rate sensitivity with respect to alpha."""

import argparse
from pathlib import Path

from refactoring_benchmark.analyze.config import PlotConfig
from refactoring_benchmark.analyze.filters import filter_results, filter_successful_only
from refactoring_benchmark.analyze.loader import discover_output_dirs, load_all_results
from refactoring_benchmark.analyze.sensitivity import (
    alpha_grid,
    compute_pass_rate_sensitivity,
    create_sensitivity_plot,
    save_sensitivity_plot,
)
from refactoring_benchmark.utils.common import load_instances_from_csv
from refactoring_benchmark.utils.paths import PSEUDO_AGENTS_DIR


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze pass-rate sensitivity vs alpha",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m refactoring_benchmark.cli.analyze_sensitivity
  python -m refactoring_benchmark.cli.analyze_sensitivity --agent-id codex-v0.77.0-gpt-5.2
  python -m refactoring_benchmark.cli.analyze_sensitivity --alpha-start 0 --alpha-end 1 --alpha-step 0.01
        """,
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        action="append",
        dest="output_dirs",
        help="Output directory containing evaluation results (can be specified multiple times).",
    )
    parser.add_argument("--agent-id", action="append", dest="agent_ids", help="Filter by agent ID.")
    parser.add_argument(
        "--description-type",
        action="append",
        dest="description_types",
        help="Filter by description type.",
    )
    parser.add_argument("--mode", action="append", dest="modes", help="Filter by inference mode.")
    parser.add_argument(
        "--successful-only",
        action="store_true",
        help="Only include inference runs with finish_reason='success'",
    )

    parser.add_argument("--alpha-start", type=float, default=0.0, help="Alpha range start (default: 0.0)")
    parser.add_argument("--alpha-end", type=float, default=1.0, help="Alpha range end (default: 1.0)")
    parser.add_argument("--alpha-step", type=float, default=0.01, help="Alpha range step (default: 0.01)")

    parser.add_argument("--no-ylabel", action="store_true", help="Hide y-axis label")
    parser.add_argument("--no-legend", action="store_true", help="Hide legend")
    parser.add_argument(
        "--legend-position",
        type=str,
        default="lower_right",
        choices=["upper_left", "upper_right", "lower_left", "lower_right"],
        help="Legend position (default: lower_right)",
    )

    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path("./instances.csv"),
        help="Path to instances.csv file (default: ./instances.csv)",
    )
    parser.add_argument(
        "--plots-dir",
        type=Path,
        default=Path("./plots/"),
        help="Directory to save plots (default: ./plots/)",
    )
    args = parser.parse_args()

    if args.output_dirs:
        output_dirs = [d.resolve() for d in args.output_dirs]
        for output_dir in output_dirs:
            if not output_dir.exists():
                print(f"Error: Output directory {output_dir} does not exist")
                return
    else:
        output_dirs = discover_output_dirs()
        if not output_dirs:
            print("Error: No directories found under ./outputs/<description_type>/<mode>")
            return

    if args.agent_ids and any(agent in {"golden_agent", "null_agent"} for agent in args.agent_ids):
        pseudo_agents_dir = PSEUDO_AGENTS_DIR
        if pseudo_agents_dir.exists() and pseudo_agents_dir not in output_dirs:
            output_dirs.append(pseudo_agents_dir)

    instances_csv = args.instances_csv.resolve()
    if not instances_csv.exists():
        print(f"Error: instances.csv not found at {instances_csv}")
        return

    try:
        instances = load_instances_from_csv(instances_csv)
    except Exception as exc:
        print(f"Error: Failed to load instances from CSV: {exc}")
        return

    if not instances:
        print("Error: No instances found in CSV")
        return

    alphas = alpha_grid(args.alpha_start, args.alpha_end, args.alpha_step)
    print(f"Alpha values: {alphas}")

    results = load_all_results(output_dirs, instances, agent_ids=args.agent_ids)
    print(f"Loaded {len(results)} evaluation results")
    if not results:
        print("No evaluation results found")
        return

    filtered_results = filter_results(
        results,
        agent_ids=args.agent_ids,
        description_types=args.description_types,
        modes=args.modes,
    )
    if args.successful_only:
        success_filter = filter_successful_only()
        filtered_results = [result for result in filtered_results if success_filter(result)]
    filtered_results = [result for result in filtered_results if result.agent_config.id not in {"null_agent"}]
    print(f"Using {len(filtered_results)} filtered evaluation results")
    if not filtered_results:
        print("No filtered evaluation results found")
        return

    sensitivity_data = compute_pass_rate_sensitivity(filtered_results, alphas=alphas)
    if not sensitivity_data:
        print("No sensitivity data to plot")
        return

    plot_config = PlotConfig(
        show_ylabel=not args.no_ylabel,
        show_legend=not args.no_legend,
        legend_position=args.legend_position,
        ytick_step=10,
    )
    fig = create_sensitivity_plot(sensitivity_data, config=plot_config)

    output_path = args.plots_dir / "pass_rate_sensitivity_alpha.pdf"
    save_sensitivity_plot(fig, output_path)
    print(f"Saved sensitivity plot to {output_path}")


if __name__ == "__main__":
    main()
