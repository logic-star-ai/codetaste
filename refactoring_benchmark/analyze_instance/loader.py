"""Load and organize evaluation results."""

from pathlib import Path
from typing import List, Sequence

from refactoring_benchmark.evaluation.models import EvaluationResult
from refactoring_benchmark.analyze_instance.models import AnalysisData, InstanceData, AgentInstanceStats
from refactoring_benchmark.analyze.validation import check_test_validity
from refactoring_benchmark.analyze.filters import ResultFilter
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


def organize_data(results: List[EvaluationResult], filters: Sequence[ResultFilter] | None = None) -> AnalysisData:
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
            commit_hash=result.instance_metadata.base_hash,
        )
        if instance.display_path not in analysis_data.instances:
            analysis_data.instances[instance.display_path] = InstanceData(instance=instance)
        # Add agent data using factory method
        agent_data = AgentInstanceStats.from_rule_metrics(result.agent_rule_metrics, validity_status)
        if result.inference_metadata is not None:
            agent_data.cost_usd = result.inference_metadata.cost_usd
        analysis_data.instances[instance.display_path].agents[agent_id] = agent_data

    return analysis_data
