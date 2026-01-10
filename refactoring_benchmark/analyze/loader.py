"""Load and organize evaluation results."""

import csv
from pathlib import Path
from typing import List, Sequence

from pydantic import ValidationError

from refactoring_benchmark.evaluation.models import EvaluationResult
from refactoring_benchmark.analyze.models import AnalysisData, InstanceData, AgentInstanceStats
from refactoring_benchmark.analyze.validation import check_test_validity
from refactoring_benchmark.analyze.filters import ResultFilter
from refactoring_benchmark.coverage.precision import calculate_precision_instance_agent
from refactoring_benchmark.utils.models import InstanceRow, ReducedInstanceRow


def load_all_results(
    output_dir: Path,
    instances: List[InstanceRow],
    agent_ids: Sequence[str] | None = None,
) -> List[EvaluationResult]:
    """
    Load evaluation_result.json files from the specified output directory.

    Args:
        output_dir: Directory to search for evaluation_result.json files
        instances: list of instances to load.

    Returns:
        List of successfully loaded EvaluationResult objects
    """
    # Create set of instance keys for fast lookup if instances provided
    if not instances:
        raise ValueError("No instances provided for loading results")

    results = []
    errors = []
    if not agent_ids:
        instance = instances[0]
        instance_dir = Path(instance.instance_dir(output_dir))
        agent_ids = [d.name for d in instance_dir.iterdir() if d.is_dir()]

    for instance in instances:
        instance_dir = Path(instance.instance_dir(output_dir))
        for agent_id in agent_ids:
            instance_agent_dir = instance_dir / agent_id / "evaluation"
            json_path = instance_agent_dir / "evaluation_result.json"
            if not json_path.is_file():
                print(f"[WARN]: Skipping missing result file: {json_path}")
                continue
            result = EvaluationResult.load_from_json(json_path)
            results.append(result)

    # Report errors at the end for cleaner output
    if errors:
        print(f"  Skipped {len(errors)} file(s) with errors:")
        for path, error in errors:
            print(f"    - {path}: {error}")

    return results


def organize_data(
    results: List[EvaluationResult],
    filters: Sequence[ResultFilter] | None = None
) -> AnalysisData:
    """
    Organize evaluation results by instance and agent, optionally applying filters.

    Args:
        results: List of evaluation results to organize
        filters: Optional list of filter functions to apply. Only results that pass
                all filters (AND logic) will be included.

    Returns:
        AnalysisData containing organized IFR metrics by instance and agent

    Example:
        >>> from refactoring_benchmark.analyze.filters import filter_by_agent_id, filter_has_execution_environment
        >>> # Only include specific agent with execution environment
        >>> data = organize_data(
        ...     results,
        ...     filters=[
        ...         filter_by_agent_id("claude-code-v2.0.76-sonnet45"),
        ...         filter_has_execution_environment(True)
        ...     ]
        ... )
    """
    analysis_data = AnalysisData()

    for result in results:
        # Apply filters if provided
        if filters:
            if not all(filter_fn(result) for filter_fn in filters):
                continue

        agent_id = result.agent_config.id

        validity_status = check_test_validity(result)
        instance = ReducedInstanceRow(
            owner=result.instance_metadata.owner, 
            repo=result.instance_metadata.repo, 
            golden_commit_hash=result.instance_metadata.golden_hash, 
            commit_hash=result.instance_metadata.base_hash
        )
        if instance.display_path not in analysis_data.instances:
            analysis_data.instances[instance.display_path] = InstanceData(instance=instance)
        # Add agent data using factory method
        agent_data = AgentInstanceStats.from_rule_metrics(
            result.agent_rule_metrics,
            validity_status
        )
        analysis_data.instances[instance.display_path].agents[agent_id] = agent_data

    return analysis_data


def load_and_merge_precision_data(
    analysis_data: AnalysisData,
    output_dir: Path,
    debug: bool = False,
) -> None:
    """
    Load precision metrics and merge them into existing analysis data.

    Modifies analysis_data in-place by adding precision metrics to AgentIFRData
    where they can be calculated.

    Args:
        analysis_data: Analysis data to merge precision into (modified in-place)
        output_dir: Base output directory containing agent results
        debug: Whether to print debug information
    """
    # Calculate precision for each instance-agent pair in analysis_data
    for instance_data in analysis_data.instances.values():
        # Calculate precision for each agent
        for agent_id, agent_data in instance_data.agents.items():
            precision_result = calculate_precision_instance_agent(
                instance_data.instance,
                agent_id,
                output_dir,
                debug=debug,
            )

            if precision_result:
                # Merge precision metrics into agent_data (convert from 0-1 to 0-100 scale)
                agent_data.precision_added = precision_result.metrics.precision_added * 100
                agent_data.precision_removed = precision_result.metrics.precision_removed * 100
                agent_data.precision_overall = precision_result.metrics.precision_overall * 100
