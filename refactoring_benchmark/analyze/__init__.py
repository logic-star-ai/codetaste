"""Analysis package for evaluation results and IFR plotting."""

from .loader import load_all_results, organize_data
from .plotting import create_ifr_plots, create_ifr_plot
from .models import AnalysisData, InstanceData, AgentIFRData
from .validation import ValidityStatus, check_test_validity
from .config import IFRPlotConfig, IFRMetricType, IFR_PLOT_DEFINITIONS
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
from .statistics import (
    MetricStatistics,
    AgentStatistics,
    CombinationStatistics,
    AllStatistics,
    compute_combination_statistics,
    compute_all_agent_statistics,
)

__all__ = [
    # Data loading and organization
    "load_all_results",
    "organize_data",
    # Plotting
    "create_ifr_plots",
    "create_ifr_plot",
    # Data models
    "AnalysisData",
    "InstanceData",
    "AgentIFRData",
    # Validation
    "ValidityStatus",
    "check_test_validity",
    # Configuration
    "IFRPlotConfig",
    "IFRMetricType",
    "IFR_PLOT_DEFINITIONS",
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
    # Statistics
    "MetricStatistics",
    "AgentStatistics",
    "CombinationStatistics",
    "AllStatistics",
    "compute_combination_statistics",
    "compute_all_agent_statistics",
]
