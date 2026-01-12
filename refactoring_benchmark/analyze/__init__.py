"""Analysis package for evaluation results - description type based analysis."""

# Data loading and organization
from .loader import (
    discover_output_dirs,
    load_all_results,
    organize_data,
    validate_analysis_data,
)

# Metrics
from .metrics import (
    METRICS,
    ALL_METRICS,
    get_metric_function,
    metric_ifr,
    metric_test_success,
)

# Data models
from .models import (
    AnalysisData,
    AgentDescriptionData,
    MetricPoint,
    AggregationType,
)

# Plotting
from .plotting import create_plot, save_plot
from .config import PlotConfig, PlotType

# Filters (keeping existing filter functionality)
from .filters import (
    ResultFilter,
    combine_filters,
    filter_by_agent_id,
    filter_by_owner,
    filter_by_repo,
    filter_by_validity_status,
    filter_has_execution_environment,
    filter_by_ifr_threshold,
    filter_by_finish_reason,
    filter_successful_only,
)

# Validation (keeping existing validation functionality)
from .validation import ValidityStatus, check_test_validity

# Utilities
from refactoring_benchmark.utils.common import load_instances_from_csv

__all__ = [
    # Data loading
    "discover_output_dirs",
    "load_all_results",
    "organize_data",
    "validate_analysis_data",
    "load_instances_from_csv",
    # Metrics
    "METRICS",
    "ALL_METRICS",
    "get_metric_function",
    "metric_ifr",
    "metric_test_success",
    # Data models
    "AnalysisData",
    "AgentDescriptionData",
    "MetricPoint",
    "AggregationType",
    # Plotting
    "create_plot",
    "save_plot",
    "PlotConfig",
    "PlotType",
    # Filters
    "ResultFilter",
    "combine_filters",
    "filter_by_agent_id",
    "filter_by_owner",
    "filter_by_repo",
    "filter_by_validity_status",
    "filter_has_execution_environment",
    "filter_by_ifr_threshold",
    "filter_by_finish_reason",
    "filter_successful_only",
    # Validation
    "ValidityStatus",
    "check_test_validity",
]
