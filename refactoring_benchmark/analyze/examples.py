"""Examples of using the analyze package with filters."""

from pathlib import Path
from refactoring_benchmark.analyze import (
    load_all_results,
    organize_data,
    create_ifr_plots,
    filter_by_agent_id,
    filter_has_execution_environment,
    filter_by_validity_status,
    filter_by_owner,
    combine_filters,
    ValidityStatus,
)


def example_basic_analysis():
    """Example: Basic analysis without filters."""
    output_dir = Path("./output")
    results = load_all_results(output_dir)
    data = organize_data(results)
    create_ifr_plots(data, Path("./analyze"))


def example_filter_single_agent():
    """Example: Analyze only one specific agent."""
    output_dir = Path("./output")
    results = load_all_results(output_dir)

    # Filter to only include Claude Code Sonnet results
    data = organize_data(results, filters=[filter_by_agent_id("claude-code-v2.0.76-sonnet45")])

    create_ifr_plots(data, Path("./analyze/claude-sonnet-only"))


def example_filter_with_exec_env():
    """Example: Analyze only instances with execution environment."""
    output_dir = Path("./output")
    results = load_all_results(output_dir)

    # Only include results where execution environment is available
    data = organize_data(results, filters=[filter_has_execution_environment(True)])

    create_ifr_plots(data, Path("./analyze/with-exec-env"))


def example_filter_valid_tests_only():
    """Example: Analyze only results with valid test results."""
    output_dir = Path("./output")
    results = load_all_results(output_dir)

    # Only include results where tests are valid
    data = organize_data(results, filters=[filter_by_validity_status(ValidityStatus.VALID)])

    create_ifr_plots(data, Path("./analyze/valid-tests-only"))


def example_filter_specific_owner():
    """Example: Analyze only specific repository owner."""
    output_dir = Path("./output")
    results = load_all_results(output_dir)

    # Only include Apache projects
    data = organize_data(results, filters=[filter_by_owner("apache")])

    create_ifr_plots(data, Path("./analyze/apache-only"))


def example_combine_multiple_filters():
    """Example: Combine multiple filters."""
    output_dir = Path("./output")
    results = load_all_results(output_dir)

    # Complex filtering: Claude Sonnet + valid tests + with execution environment
    data = organize_data(
        results,
        filters=[
            filter_by_agent_id("claude-code-v2.0.76-sonnet45"),
            filter_by_validity_status(ValidityStatus.VALID),
            filter_has_execution_environment(True),
        ],
    )

    create_ifr_plots(data, Path("./analyze/claude-valid-with-env"))


def example_using_combine_filters():
    """Example: Use combine_filters helper for reusable filter combinations."""
    output_dir = Path("./output")
    results = load_all_results(output_dir)

    # Create a reusable combined filter
    production_ready_filter = combine_filters(
        filter_has_execution_environment(True), filter_by_validity_status(ValidityStatus.VALID)
    )

    # Can use this filter as a single function
    data = organize_data(results, filters=[production_ready_filter])

    create_ifr_plots(data, Path("./analyze/production-ready"))


def example_filter_successful_runs():
    """Example: Only include successful inference runs."""
    from refactoring_benchmark.analyze import filter_successful_only

    output_dir = Path("./output")
    results = load_all_results(output_dir)

    # Only include runs where finish_reason="success"
    data = organize_data(results, filters=[filter_successful_only()])

    create_ifr_plots(data, Path("./analyze/successful-only"))


def example_filter_by_finish_reason():
    """Example: Filter by specific finish reasons."""
    from refactoring_benchmark.analyze import filter_by_finish_reason

    output_dir = Path("./output")
    results = load_all_results(output_dir)

    # Include success or max_turns (exclude crashed, error, etc.)
    data = organize_data(results, filters=[filter_by_finish_reason(["success", "max_turns"])])

    create_ifr_plots(data, Path("./analyze/success-or-max-turns"))


def example_high_quality_results():
    """Example: Combine multiple filters for high-quality results only."""
    from refactoring_benchmark.analyze import filter_successful_only

    output_dir = Path("./output")
    results = load_all_results(output_dir)

    # Only include: successful runs + valid tests + with execution environment
    data = organize_data(
        results,
        filters=[
            filter_successful_only(),
            filter_by_validity_status(ValidityStatus.VALID),
            filter_has_execution_environment(True),
        ],
    )

    create_ifr_plots(data, Path("./analyze/high-quality"))


if __name__ == "__main__":
    # Run basic example
    print("Running basic analysis example...")
    example_basic_analysis()
