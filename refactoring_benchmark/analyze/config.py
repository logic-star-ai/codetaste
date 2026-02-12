"""Configuration for description-type based analysis plotting."""

from typing import Literal

from pydantic import BaseModel, Field

PlotType = Literal["line", "bar", "scatter"]


class PlotConfig(BaseModel):
    """Configuration for description-type analysis plots."""

    # Plot dimensions
    width: int = Field(default=10, ge=1, description="Plot width in inches")
    height: int = Field(default=6, ge=1, description="Plot height in inches")

    # Line plot settings
    line_width: float = Field(default=2.0, gt=0, description="Line width for line plots")
    marker_size: float = Field(default=8.0, gt=0, description="Marker size")
    marker_style: str = Field(default="o", description="Marker style (o, s, ^, etc.)")
    alpha: float = Field(default=0.8, ge=0, le=1, description="Transparency")

    # Bar plot settings
    bar_width: float = Field(default=0.8, gt=0, le=1, description="Bar width ratio")
    bar_alpha: float = Field(default=0.8, ge=0, le=1, description="Bar transparency")

    # Error bar settings
    show_error_bars: bool = Field(default=True, description="Show Standard Error error bars")
    error_bar_capsize: float = Field(default=5.0, ge=0, description="Error bar cap size")
    error_bar_alpha: float = Field(default=0.5, ge=0, le=1, description="Error bar transparency")

    # Text settings
    show_ylabel: bool = Field(default=True, description="Show y-axis label")
    show_legend: bool = Field(default=True, description="Show legend")
    legend_position: Literal["upper_left", "upper_right", "lower_left"] = Field(
        default="upper_left", description="Legend position (upper_left, upper_right, lower_left)"
    )
    xlabel_fontsize: int = Field(default=21, ge=1, description="X-axis label font size")
    ylabel_fontsize: int = Field(default=20, ge=1, description="Y-axis label font size")
    title_fontsize: int = Field(default=23, ge=1, description="Title font size")
    tick_fontsize: int = Field(default=19, ge=1, description="Tick label font size")
    legend_fontsize: int = Field(default=18, ge=1, description="Legend font size")

    # Grid settings
    grid_alpha: float = Field(default=0.3, ge=0, le=1, description="Grid transparency")
    grid_linestyle: str = Field(default="--", description="Grid line style")

    # Y-axis limits
    ylim_min: float = Field(default=0.0, description="Y-axis minimum")
    ylim_max: float = Field(default=1.0, description="Y-axis maximum")
    ytick_step: int = Field(default=5, ge=1, description="Y-axis tick step (percent)")

    class Config:
        frozen = True  # Make immutable
