"""Tests for policy comparisons."""

from s004 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    MonteCarloComparisonConfig,
    ObjectiveFunction,
    compare_policies,
)
from tests.support import create_competing_parameters


def test_comparison_includes_each_policy_with_distinct_metrics() -> None:
    """Return one deterministic comparison row for every named policy."""
    comparisons = compare_policies(
        create_competing_parameters(),
        {"debt_first": DebtFirstPolicy(), "backlog_first": BacklogFirstPolicy()},
        ObjectiveFunction(),
    )

    assert tuple(comparison.name for comparison in comparisons) == (
        "debt_first",
        "backlog_first",
    )
    assert (
        comparisons[0].metrics["final_backlog"].mean
        != comparisons[1].metrics["final_backlog"].mean
    )


def test_comparison_supports_monte_carlo_results() -> None:
    """Return a Monte Carlo comparison row for every named policy."""
    comparisons = compare_policies(
        MonteCarloComparisonConfig(2, 7, create_competing_parameters()),
        {"debt_first": DebtFirstPolicy(), "backlog_first": BacklogFirstPolicy()},
        ObjectiveFunction(),
    )

    assert len(comparisons) == 2
    assert all(
        comparison.monte_carlo_simulation is not None for comparison in comparisons
    )
    assert all(
        comparison.deterministic_trajectory is None for comparison in comparisons
    )
