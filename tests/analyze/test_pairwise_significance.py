import math
from argparse import Namespace

import pytest

from refactoring_benchmark.analyze.models import AnalysisData
from refactoring_benchmark.analyze.pairwise_significance import (
    _oriented_summary_fields,
    align_paired_points,
    analyze_metric_significance,
    apply_benjamini_hochberg,
    build_mermaid_diagram,
    build_significance_win_loss_summary,
    paired_permutation_p_value,
    render_markdown_report,
    stable_seed,
    validate_args,
)


def test_paired_permutation_ignores_tied_pairs() -> None:
    p_value, method, permutations = paired_permutation_p_value(
        [1.0, 1.0, 0.0],
        permutations=100,
        exact_threshold=10,
        seed=0,
    )

    assert p_value == pytest.approx(0.5)
    assert method == "exact"
    assert permutations == 4


def test_paired_permutation_less_uses_lower_tail() -> None:
    p_value, method, permutations = paired_permutation_p_value(
        [-2.0, 1.0],
        alternative="less",
        permutations=100,
        exact_threshold=10,
        seed=0,
    )

    assert p_value == pytest.approx(0.5)
    assert method == "exact"
    assert permutations == 4


def test_benjamini_hochberg_preserves_input_order() -> None:
    assert apply_benjamini_hochberg([0.03, 0.01, 0.2]) == pytest.approx([0.045, 0.03, 0.2])


def test_stable_seed_is_deterministic_and_identity_dependent() -> None:
    seed = stable_seed("ifr", "open", "direct", "agent_a", "agent_b", base_seed=0)

    assert seed == stable_seed("ifr", "open", "direct", "agent_a", "agent_b", base_seed=0)
    assert seed != stable_seed("ifr", "open", "direct", "agent_a", "agent_c", base_seed=0)


def test_analyze_metric_significance_aligns_shared_instances() -> None:
    data = AnalysisData()
    data.add_metric_point("agent_a", "open", "plan", "shared_1", 1.0)
    data.add_metric_point("agent_a", "open", "plan", "shared_2", 1.0)
    data.add_metric_point("agent_a", "open", "plan", "only_a", 1.0)
    data.add_metric_point("agent_b", "open", "plan", "shared_1", 0.0)
    data.add_metric_point("agent_b", "open", "plan", "shared_2", 1.0)
    data.add_metric_point("agent_b", "open", "plan", "only_b", 0.0)

    comparisons = analyze_metric_significance(
        data,
        metric="ifr",
        alpha=0.05,
        permutations=100,
        bootstrap_resamples=100,
        exact_threshold=10,
        seed=0,
    )

    assert len(comparisons) == 1
    comparison = comparisons[0]
    assert {comparison.model_a, comparison.model_b} == {"agent_a", "agent_b"}
    assert comparison.observed_n_pairs == 2
    assert comparison.n_pairs == 2
    assert comparison.better_model == "agent_a"
    assert comparison.observed_direction == "agent_a > agent_b"
    assert "observed_direction" in comparison.to_dict()
    assert "p_value_direction" not in comparison.to_dict()
    assert abs(comparison.mean_difference) == pytest.approx(0.5)
    assert max(comparison.wins_a, comparison.wins_b) == 1
    assert comparison.ties == 1
    assert min(comparison.wins_a, comparison.wins_b) == 0


def test_align_paired_points_rejects_duplicate_instance_keys() -> None:
    data = AnalysisData()
    data.add_metric_point("agent_a", "open", "direct", "shared", 1.0)
    data.add_metric_point("agent_a", "open", "direct", "shared", 0.5)
    data.add_metric_point("agent_b", "open", "direct", "shared", 0.0)

    data_a = data.get_data("agent_a", "open", "direct")
    data_b = data.get_data("agent_b", "open", "direct")
    assert data_a is not None
    assert data_b is not None
    with pytest.raises(ValueError, match="Duplicate metric value"):
        align_paired_points(data_a, data_b)


def test_align_paired_points_rejects_non_finite_shared_values() -> None:
    data = AnalysisData()
    data.add_metric_point("agent_a", "open", "direct", "shared", math.nan)
    data.add_metric_point("agent_b", "open", "direct", "shared", 0.0)

    data_a = data.get_data("agent_a", "open", "direct")
    data_b = data.get_data("agent_b", "open", "direct")
    assert data_a is not None
    assert data_b is not None
    with pytest.raises(ValueError, match="Non-finite metric value"):
        align_paired_points(data_a, data_b)


def test_zero_mean_non_tie_uses_clear_method_name() -> None:
    data = AnalysisData()
    data.add_metric_point("agent_a", "open", "direct", "shared_1", 1.0)
    data.add_metric_point("agent_a", "open", "direct", "shared_2", 0.0)
    data.add_metric_point("agent_b", "open", "direct", "shared_1", 0.0)
    data.add_metric_point("agent_b", "open", "direct", "shared_2", 1.0)

    comparisons = analyze_metric_significance(
        data,
        metric="ifr",
        alpha=0.05,
        permutations=100,
        bootstrap_resamples=100,
        exact_threshold=10,
        seed=0,
    )

    assert len(comparisons) == 1
    comparison = comparisons[0]
    assert comparison.mean_difference == pytest.approx(0.0)
    assert comparison.permutation_method == "zero_mean_difference"
    assert comparison.wins_a == 1
    assert comparison.ties == 0
    assert comparison.wins_b == 1


def test_analyze_metric_significance_treats_tiny_differences_as_ties() -> None:
    data = AnalysisData()
    data.add_metric_point("agent_a", "open", "direct", "shared", 1.0)
    data.add_metric_point("agent_b", "open", "direct", "shared", 1.0 + 1e-13)

    comparisons = analyze_metric_significance(
        data,
        metric="ifr",
        alpha=0.05,
        permutations=100,
        bootstrap_resamples=100,
        exact_threshold=10,
        seed=0,
    )

    assert len(comparisons) == 1
    comparison = comparisons[0]
    assert comparison.better_model is None
    assert comparison.worse_model is None
    assert comparison.wins_a == 0
    assert comparison.ties == 1
    assert comparison.wins_b == 0
    assert comparison.p_value == pytest.approx(1.0)


def test_oriented_summary_fields_preserves_zero_mean_win_loss_counts() -> None:
    row = {
        "better_model": None,
        "model_a": "agent_a",
        "model_b": "agent_b",
        "mean_difference": 0.0,
        "ci_low": -0.2,
        "ci_high": 0.2,
        "wins_a": 50,
        "ties": 0,
        "wins_b": 50,
    }

    assert _oriented_summary_fields(row) == (0.0, -0.2, 0.2, 50, 0, 50)


def test_build_significance_win_loss_summary_counts_corrected_outcomes() -> None:
    report = {
        "metadata": {"metrics": ["ifr_x_test_success"], "alpha": 0.05},
        "metrics": {
            "ifr_x_test_success": [
                {
                    "description_type": "open",
                    "mode": "direct",
                    "model_a": "agent_a",
                    "model_b": "agent_b",
                    "better_model": "agent_a",
                    "worse_model": "agent_b",
                    "is_significant": True,
                    "n_pairs": 100,
                },
                {
                    "description_type": "open",
                    "mode": "direct",
                    "model_a": "agent_a",
                    "model_b": "agent_c",
                    "better_model": "agent_a",
                    "worse_model": "agent_c",
                    "is_significant": False,
                    "n_pairs": 100,
                },
                {
                    "description_type": "open",
                    "mode": "direct",
                    "model_a": "agent_b",
                    "model_b": "agent_c",
                    "better_model": "agent_c",
                    "worse_model": "agent_b",
                    "is_significant": True,
                    "n_pairs": 100,
                },
            ]
        },
    }

    agents, rows = build_significance_win_loss_summary(report)

    assert agents == ["agent_a", "agent_b", "agent_c"]
    assert len(rows) == 1
    counts = rows[0]["counts"]
    assert counts["agent_a"] == {"wins": 1, "losses": 0}
    assert counts["agent_b"] == {"wins": 0, "losses": 2}
    assert counts["agent_c"] == {"wins": 1, "losses": 0}


def test_mermaid_diagram_escapes_quoted_labels() -> None:
    diagram = build_mermaid_diagram(
        "ifr",
        "open",
        "direct",
        [
            {
                "model_a": "agent_a",
                "model_b": "agent_b",
                "model_a_label": 'Agent "A"',
                "model_b_label": r"Agent \B",
                "better_model": "agent_a",
                "worse_model": "agent_b",
                "better_model_label": 'Agent "A"',
                "worse_model_label": r"Agent \B",
                "is_significant": True,
            }
        ],
    )

    assert '["Agent \\"A\\""]' in diagram
    assert r'["Agent \\B"]' in diagram


def test_markdown_report_uses_neutral_model_columns_for_tie_rows() -> None:
    report = {
        "metadata": {
            "metrics": ["ifr"],
            "alpha": 0.05,
            "n_results_after_filtering": 2,
            "successful_only": False,
        },
        "metrics": {
            "ifr": [
                {
                    "description_type": "open",
                    "description_type_label": "Open",
                    "mode": "direct",
                    "mode_label": "Direct",
                    "model_a": "agent_a",
                    "model_a_label": "Agent A",
                    "model_b": "agent_b",
                    "model_b_label": "Agent B",
                    "better_model": None,
                    "better_model_label": None,
                    "worse_model": None,
                    "worse_model_label": None,
                    "mean_a": 0.5,
                    "mean_b": 0.5,
                    "mean_difference": 0.0,
                    "ci_low": -0.1,
                    "ci_high": 0.1,
                    "wins_a": 1,
                    "ties": 0,
                    "wins_b": 1,
                    "n_pairs": 2,
                    "p_value": 1.0,
                    "q_value": 1.0,
                    "is_significant": False,
                }
            ]
        },
    }

    rendered = render_markdown_report(report)

    assert "| Model 1 | Model 2 | N | Mean 1 | Mean 2 |" in rendered
    assert "| Better | Worse |" not in rendered
    assert "| Agent A | Agent B | 2 | 50.00% | 50.00% | 0.00 pp | [-10.00, 10.00] pp | 1/0/1 |" in rendered


def test_validate_args_rejects_invalid_numeric_values() -> None:
    valid = Namespace(alpha=0.05, permutations=100, bootstrap_resamples=100, exact_threshold=0)
    validate_args(valid)

    for field, value in [
        ("alpha", 0.0),
        ("alpha", 1.01),
        ("permutations", 0),
        ("bootstrap_resamples", 0),
        ("exact_threshold", -1),
    ]:
        args = Namespace(alpha=0.05, permutations=100, bootstrap_resamples=100, exact_threshold=0)
        setattr(args, field, value)
        with pytest.raises(SystemExit):
            validate_args(args)
