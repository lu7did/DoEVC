"""Tests for deterministic and Monte Carlo policy comparisons."""

from doevc_s001 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    ModelParameters,
    MonteCarloComparisonConfig,
    ObjectiveFunction,
    compare_policies,
)


def test_comparison_includes_each_policy_with_distinct_deterministic_metrics() -> None:
    """Return one deterministic row per policy with its C3 metrics."""
    comparisons = compare_policies(
        _parameters_with_backlog_and_debt(),
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


def test_comparison_supports_reproducible_monte_carlo_results() -> None:
    """Return a Monte Carlo comparison row for every named policy."""
    config = MonteCarloComparisonConfig(
        n_runs=2,
        seed=7,
        base_parameters=_parameters_with_backlog_and_debt(),
    )

    comparisons = compare_policies(
        config,
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


def _parameters_with_backlog_and_debt() -> ModelParameters:
    """Return a one-sprint scenario where policies have distinct outcomes."""
    return ModelParameters(
        B0=10.0,
        D0=10.0,
        V0=10.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.0,
        lambda_=0.0,
        rho=0.0,
        K=1,
        s=1.0,
    )
