import numpy as np

from refactoring_benchmark.analyze.config import PlotConfig
from refactoring_benchmark.analyze.plotting import _resolve_y_axis


def test_resolve_y_axis_rounds_percent_metrics_up_to_tick_by_default() -> None:
    ylim_max, y_ticks = _resolve_y_axis("ifr", PlotConfig(ylim_max=1.0, ytick_step=6))

    assert ylim_max == 102.0
    assert np.array_equal(y_ticks, np.arange(0, 105.0, 6.0))


def test_resolve_y_axis_can_force_percent_metrics_to_exactly_100() -> None:
    ylim_max, y_ticks = _resolve_y_axis("ifr", PlotConfig(ylim_max=1.0, ytick_step=6, force_percent_ylim_100=True))

    assert ylim_max == 100.0
    assert np.array_equal(y_ticks, np.arange(0, 103.0, 6.0))


def test_resolve_y_axis_does_not_force_non_percent_metrics() -> None:
    ylim_max, y_ticks = _resolve_y_axis(
        "cost",
        PlotConfig(ylim_max=1.0, ytick_step=6, force_percent_ylim_100=True),
    )

    assert ylim_max == 1.02
    assert np.array_equal(y_ticks, np.arange(0, 1.05, 0.06))
