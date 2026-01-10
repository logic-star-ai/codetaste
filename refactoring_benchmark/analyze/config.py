"""Configuration for analysis plotting."""

from typing import Literal
from pydantic import BaseModel, Field


class IFRPlotConfig(BaseModel):
    """Configuration for IFR (Instruction Following Rate) plots."""

    # Plot dimensions
    min_width: int = Field(default=12, ge=1, description="Minimum plot width in inches")
    width_per_instance: float = Field(default=0.8, gt=0, description="Width per instance in inches")
    height: int = Field(default=6, ge=1, description="Plot height in inches")

    # Bar settings
    bar_width_ratio: float = Field(default=0.8, gt=0, le=1, description="Fraction of space used by bars")
    bar_alpha: float = Field(default=0.8, ge=0, le=1, description="Bar transparency (0=transparent, 1=opaque)")

    # Hatch patterns for invalid results
    hatch_pattern: str = Field(default="///", description="Hatch pattern for invalid results")
    invalid_tests_edge_color: str = Field(default="red", description="Edge color for invalid test results")
    no_exec_env_edge_color: str = Field(default="black", description="Edge color for no execution environment")
    no_test_results_edge_color: str = Field(default="gray", description="Edge color for no test results")
    edge_linewidth: float = Field(default=1.5, gt=0, description="Line width for hatched edges")

    # Text settings
    xlabel_fontsize: int = Field(default=10, ge=1, description="X-axis label font size")
    ylabel_fontsize: int = Field(default=10, ge=1, description="Y-axis label font size")
    title_fontsize: int = Field(default=12, ge=1, description="Title font size")
    tick_fontsize: int = Field(default=8, ge=1, description="Tick label font size")
    legend_fontsize: int = Field(default=8, ge=1, description="Legend font size")
    footer_fontsize: int = Field(default=8, ge=1, description="Footer text font size")

    # Grid settings
    grid_alpha: float = Field(default=0.3, ge=0, le=1, description="Grid transparency")
    grid_linestyle: str = Field(default="--", description="Grid line style")

    # Footer text
    footer_text: str = Field(
        default="Red hatching: invalid test results | Black hatching: no execution environment",
        description="Footer text explaining hatching patterns",
    )

    class Config:
        frozen = True  # Make immutable like the dataclass was


IFRMetricType = Literal["positive_ifr", "negative_ifr", "total_ifr"]


IFR_PLOT_DEFINITIONS: list[tuple[IFRMetricType, str]] = [
    ("positive_ifr", "Positive Instruction Following Rate by Agent"),
    ("negative_ifr", "Negative Instruction Following Rate by Agent"),
    ("total_ifr", "Total Instruction Following Rate by Agent"),
]
