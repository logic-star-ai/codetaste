"""Filtering system for evaluation results."""

from typing import Callable, Sequence

from refactoring_benchmark.analyze.validation import ValidityStatus, check_test_validity
from refactoring_benchmark.evaluation.models import EvaluationResult

# Type alias for filter functions
ResultFilter = Callable[[EvaluationResult], bool]


def combine_filters(*filters: ResultFilter) -> ResultFilter:
    """
    Combine multiple filters with AND logic.

    Args:
        *filters: Variable number of filter functions

    Returns:
        A single filter function that returns True only if all filters return True
    """

    def combined(result: EvaluationResult) -> bool:
        return all(f(result) for f in filters)

    return combined


def filter_results(
    results: Sequence[EvaluationResult],
    agent_ids: Sequence[str] | None = None,
    description_types: Sequence[str] | None = None,
    modes: Sequence[str] | None = None,
) -> list[EvaluationResult]:
    """Filter evaluation results by agent, description type, and mode."""
    filtered = []
    for result in results:
        if agent_ids and result.agent_config.id not in agent_ids:
            continue

        if description_types or modes:
            metadata = result.inference_metadata
            if metadata is None:
                continue
            if description_types and metadata.description_type not in description_types:
                continue
            if modes and metadata.mode not in modes:
                continue
        filtered.append(result)
    return filtered


# Common filter builders


def filter_by_agent_id(agent_ids: str | Sequence[str]) -> ResultFilter:
    """
    Create a filter that accepts only specified agent IDs.

    Args:
        agent_ids: Single agent ID or sequence of agent IDs to include

    Returns:
        Filter function

    Example:
        >>> filter_fn = filter_by_agent_id("claude-code-v2.0.76-sonnet45")
        >>> filter_fn = filter_by_agent_id(["agent1", "agent2"])
    """
    if isinstance(agent_ids, str):
        agent_ids = [agent_ids]
    agent_set = set(agent_ids)

    def filter_fn(result: EvaluationResult) -> bool:
        return result.agent_config.id in agent_set

    return filter_fn


def filter_no_timeouts() -> ResultFilter:
    """
    Create a filter that excludes results which timed out during execution.

    Returns:
        Filter function

    Example:
        >>> filter_fn = filter_no_timeouts()
    """

    def filter_fn(result: EvaluationResult) -> bool:
        return result.inference_metadata.finish_reason != "timeout"

    return filter_fn


def filter_by_owner(owners: str | Sequence[str]) -> ResultFilter:
    """
    Create a filter that accepts only specified repository owners.

    Args:
        owners: Single owner or sequence of owners to include

    Returns:
        Filter function

    Example:
        >>> filter_fn = filter_by_owner("apache")
        >>> filter_fn = filter_by_owner(["apache", "golang"])
    """
    if isinstance(owners, str):
        owners = [owners]
    owner_set = set(owners)

    def filter_fn(result: EvaluationResult) -> bool:
        return result.instance_metadata.owner in owner_set

    return filter_fn


def filter_by_repo(repos: str | Sequence[str]) -> ResultFilter:
    """
    Create a filter that accepts only specified repositories.

    Args:
        repos: Single repo or sequence of repos to include

    Returns:
        Filter function

    Example:
        >>> filter_fn = filter_by_repo("arrow")
        >>> filter_fn = filter_by_repo(["arrow", "spark"])
    """
    if isinstance(repos, str):
        repos = [repos]
    repo_set = set(repos)

    def filter_fn(result: EvaluationResult) -> bool:
        return result.instance_metadata.repo in repo_set

    return filter_fn


def filter_by_validity_status(statuses: ValidityStatus | Sequence[ValidityStatus]) -> ResultFilter:
    """
    Create a filter that accepts only specified validity statuses.

    Args:
        statuses: Single status or sequence of statuses to include

    Returns:
        Filter function

    Example:
        >>> filter_fn = filter_by_validity_status(ValidityStatus.VALID)
        >>> filter_fn = filter_by_validity_status([ValidityStatus.VALID, ValidityStatus.NO_EXEC_ENV])
    """
    if isinstance(statuses, ValidityStatus):
        statuses = [statuses]
    status_set = set(statuses)

    def filter_fn(result: EvaluationResult) -> bool:
        return check_test_validity(result) in status_set

    return filter_fn


def filter_has_execution_environment(has_env: bool = True) -> ResultFilter:
    """
    Create a filter based on execution environment availability.

    Args:
        has_env: If True, include only results with execution environment.
                 If False, include only results without execution environment.

    Returns:
        Filter function

    Example:
        >>> filter_fn = filter_has_execution_environment(True)  # Only with exec env
        >>> filter_fn = filter_has_execution_environment(False)  # Only without exec env
    """

    def filter_fn(result: EvaluationResult) -> bool:
        return result.instance_metadata.has_execution_environment == has_env

    return filter_fn


def filter_by_ifr_threshold(
    metric: str = "ifr", min_value: float | None = None, max_value: float | None = None
) -> ResultFilter:
    """
    Create a filter based on IFR metric thresholds.

    Args:
        metric: Metric to check ("ifr", "positive_ifr", or "negative_ifr")
        min_value: Minimum IFR value (0-1 scale), inclusive
        max_value: Maximum IFR value (0-1 scale), inclusive

    Returns:
        Filter function

    Example:
        >>> filter_fn = filter_by_ifr_threshold("ifr", min_value=0.8)  # IFR >= 80%
        >>> filter_fn = filter_by_ifr_threshold("positive_ifr", min_value=0.5, max_value=0.9)
    """

    def filter_fn(result: EvaluationResult) -> bool:
        value = getattr(result.agent_rule_metrics, metric)
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True

    return filter_fn


def filter_by_finish_reason(finish_reasons: str | Sequence[str]) -> ResultFilter:
    """
    Create a filter based on inference finish reason.

    Args:
        finish_reasons: Single finish reason or list of acceptable finish reasons
                       (e.g., "success", ["success", "max_turns"])

    Returns:
        Filter function that checks finish_reason in inference_metadata

    Example:
        >>> # Only include successful runs
        >>> data = organize_data(results, filters=[filter_by_finish_reason("success")])
        >>>
        >>> # Include success or max_turns
        >>> data = organize_data(results, filters=[filter_by_finish_reason(["success", "max_turns"])])
    """
    if isinstance(finish_reasons, str):
        finish_reasons = [finish_reasons]
    reason_set = set(finish_reasons)

    def filter_fn(result: EvaluationResult) -> bool:
        # If no inference metadata, exclude by default
        if result.inference_metadata is None:
            return False
        return result.inference_metadata.finish_reason in reason_set

    return filter_fn


def filter_successful_only() -> ResultFilter:
    """
    Convenience filter to only include successful inference runs.

    Equivalent to filter_by_finish_reason("success").

    Returns:
        Filter function that only accepts finish_reason="success"

    Example:
        >>> data = organize_data(results, filters=[filter_successful_only()])
    """
    return filter_by_finish_reason("success")
