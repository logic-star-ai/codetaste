"""Load and organize evaluation results for description-type based analysis."""

from pathlib import Path
from typing import Sequence

from refactoring_benchmark.evaluation.models import EvaluationResult
from refactoring_benchmark.analyze.models import AnalysisData
from refactoring_benchmark.analyze.metrics import get_metric_function
from refactoring_benchmark.analyze.filters import ResultFilter
from refactoring_benchmark.utils.models import InstanceRow


def discover_output_dirs(cwd: Path = Path.cwd()) -> list[Path]:
    """Discover all directories starting with 'output' in the current working directory.

    Args:
        cwd: Working directory to search (defaults to current directory)

    Returns:
        List of directories matching 'output*' pattern, sorted by name
    """
    return sorted([d for d in cwd.iterdir() if d.is_dir() and d.name.startswith("output")])


def load_all_results(
    output_dirs: list[Path],
    instances: list[InstanceRow],
    agent_ids: Sequence[str] | None = None,
) -> list[EvaluationResult]:
    """Load evaluation_result.json files from multiple output directories.

    Args:
        output_dirs: List of directories to search for evaluation_result.json files
        instances: List of instances to load
        agent_ids: Optional list of agent IDs to load (defaults to all agents in first directory)

    Returns:
        List of successfully loaded EvaluationResult objects
    """
    if not instances:
        raise ValueError("No instances provided for loading results")

    results = []
    errors = []

    # If no agent_ids specified, discover them from the first output_dir
    if not agent_ids:
        instance = instances[0]
        instance_dir = Path(instance.instance_dir(output_dirs[0]))
        if instance_dir.exists():
            agent_ids = [d.name for d in instance_dir.iterdir() if d.is_dir()]
        else:
            agent_ids = []


    # Load from all output directories
    for output_dir in output_dirs:
        for instance in instances:
            instance_dir = Path(instance.instance_dir(output_dir))
            if not instance_dir.exists():
                continue

            for agent_id in agent_ids:
                instance_agent_dir = instance_dir / agent_id / "evaluation"
                json_path = instance_agent_dir / "evaluation_result.json"
                if not json_path.is_file():
                    continue

                try:
                    result = EvaluationResult.load_from_json(json_path)
                    results.append(result)
                except Exception as e:
                    errors.append((json_path, str(e)))

    # Report errors at the end for cleaner output
    if errors:
        print(f"  Skipped {len(errors)} file(s) with errors:")
        for path, error in errors:
            print(f"    - {path}: {error}")

    return results


def organize_data(
    results: list[EvaluationResult],
    metric_name: str,
    filters: Sequence[ResultFilter] | None = None,
) -> AnalysisData:
    """Organize evaluation results by (agent_id, description_type) with the given metric.

    Args:
        results: List of evaluation results to organize
        metric_name: Name of the metric to extract (e.g., "ifr", "test_success", "precision_overall")
        filters: Optional list of filter functions to apply (AND logic)

    Returns:
        AnalysisData containing organized metric values grouped by agent and description type

    Example:
        >>> from refactoring_benchmark.analyze.filters import filter_successful_only
        >>> data = organize_data(results, "ifr", filters=[filter_successful_only()])
    """
    # Get metric function
    metric_fn = get_metric_function(metric_name)
    analysis_data = AnalysisData()

    for result in results:
        # Apply filters if provided
        if filters:
            if not all(filter_fn(result) for filter_fn in filters):
                continue

        # Extract agent_id and description_type
        agent_id = result.agent_config.id
        description_type = "standard"  # Default
        if result.inference_metadata and result.inference_metadata.description_type:
            description_type = result.inference_metadata.description_type

        # Extract metric value
        metric_value = metric_fn(result)
        if metric_value is None:
            # Skip this result if metric cannot be computed
            continue

        # Create instance key
        instance_key = f"{result.instance_metadata.owner}/{result.instance_metadata.repo}/{result.instance_metadata.base_hash[:8]}"

        # Add to analysis data
        analysis_data.add_metric_point(agent_id, description_type, instance_key, metric_value)

    return analysis_data


def validate_analysis_data(
    data: AnalysisData,
    agent_ids: list[str] | None = None,
    description_types: list[str] | None = None,
) -> None:
    """Validate analysis data and print warnings/errors about missing combinations.

    Args:
        data: Analysis data to validate
        agent_ids: Expected agent IDs (defaults to all found in data)
        description_types: Expected description types (defaults to all found in data)

    Raises:
        ValueError: If an expected agent has no data at all
    """
    if agent_ids is None:
        agent_ids = data.get_agent_ids()
    if description_types is None:
        description_types = data.get_description_types()

    # Check for completely missing agents
    for agent_id in agent_ids:
        agent_data = [v for k, v in data.data.items() if k[0] == agent_id]
        if not agent_data:
            available_agents = ", ".join(data.get_agent_ids())
            raise ValueError(
                f"Agent '{agent_id}' has no data. Available agents: {available_agents}\n"
                f"Hint: Use --agent-id flag to specify available agents."
            )

    # Check for missing description types and print warnings
    max_count_per_agent = {}
    for agent_id in agent_ids:
        counts = []
        for desc_type in description_types:
            agent_desc_data = data.get_data(agent_id, desc_type)
            if agent_desc_data:
                counts.append(agent_desc_data.count)
        max_count_per_agent[agent_id] = max(counts) if counts else 0

    overall_max = max(max_count_per_agent.values()) if max_count_per_agent else 0

    for agent_id in agent_ids:
        agent_max = max_count_per_agent.get(agent_id, 0)
        if agent_max < overall_max:
            print(
                f"WARNING: Agent '{agent_id}' has fewer data points ({agent_max}) "
                f"than other agents ({overall_max})"
            )            

        # Check which description types are missing
        missing_desc_types = []
        for desc_type in description_types:
            agent_desc_data = data.get_data(agent_id, desc_type)
            if not agent_desc_data or agent_desc_data.count == 0:
                missing_desc_types.append(desc_type)

        if missing_desc_types:
            print(f"WARNING: Agent '{agent_id}' missing data for: {', '.join(missing_desc_types)}")
