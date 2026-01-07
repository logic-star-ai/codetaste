"""Load and organize evaluation results."""

from pathlib import Path
from typing import List, Sequence

from pydantic import ValidationError

from refactoring_benchmark.evaluation.models import EvaluationResult
from refactoring_benchmark.analyze.models import AnalysisData, InstanceData, AgentIFRData
from refactoring_benchmark.analyze.validation import check_test_validity
from refactoring_benchmark.analyze.filters import ResultFilter


def load_all_results(output_dir: Path) -> List[EvaluationResult]:
    """
    Load all evaluation_result.json files from the specified output directory.

    Args:
        output_dir: Directory to search for evaluation_result.json files

    Returns:
        List of successfully loaded EvaluationResult objects
    """
    results = []
    errors = []

    for json_path in output_dir.rglob("evaluation_result.json"):
        try:
            results.append(EvaluationResult.load_from_json(json_path))
        except ValidationError as e:
            # Extract the main error for cleaner output
            error_msg = e.errors()[0]["type"] if e.errors() else "validation error"
            errors.append((json_path.relative_to(output_dir), error_msg))
        except Exception as e:
            errors.append((json_path.relative_to(output_dir), type(e).__name__))

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

        meta = result.instance_metadata
        instance_key = f"{meta.owner}/{meta.repo}/{meta.base_hash[:8]}"
        agent_id = result.agent_config.id

        validity_status = check_test_validity(result)

        # Create or get instance data
        if instance_key not in analysis_data.instances:
            analysis_data.instances[instance_key] = InstanceData(instance_key=instance_key)

        # Add agent data using factory method
        agent_data = AgentIFRData.from_rule_metrics(
            result.agent_rule_metrics,
            validity_status
        )
        analysis_data.instances[instance_key].agents[agent_id] = agent_data

    return analysis_data
