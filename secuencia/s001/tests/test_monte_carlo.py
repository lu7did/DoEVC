"""Tests for Monte Carlo simulation runs."""

import pytest

from doevc_s001 import (
    DebtFirstPolicy,
    MetricSummary,
    ModelParameters,
    MonteCarloResult,
    aggregate_metrics,
    run_monte_carlo,
)


def base_parameters() -> ModelParameters:
    """Return a compact deterministic model for Monte Carlo tests."""
    return ModelParameters(
        B0=8.0,
        D0=4.0,
        V0=4.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=3,
        s=1.0,
    )


def test_monte_carlo_runs_are_reproducible_with_a_fixed_seed() -> None:
    """Return equal individual runs and summary from the same seed."""
    first = run_monte_carlo(
        3,
        DebtFirstPolicy(),
        seed=1234,
        base_parameters=base_parameters(),
    )
    second = run_monte_carlo(
        3,
        DebtFirstPolicy(),
        seed=1234,
        base_parameters=base_parameters(),
    )

    assert first == second


def test_monte_carlo_executes_exactly_the_requested_number_of_runs() -> None:
    """Store one individual result and final state per requested run."""
    result = run_monte_carlo(
        4,
        DebtFirstPolicy(),
        seed=7,
        base_parameters=base_parameters(),
    )

    assert len(result.runs) == 4
    assert result.summary.run_count == 4
    assert len(result.summary.final_backlogs) == 4
    assert len(result.summary.final_technical_debts) == 4
    assert all(run.trajectory[0].remediation_fraction == 1.0 for run in result.runs)


def test_monte_carlo_rejects_non_positive_run_counts() -> None:
    """Reject requests that cannot execute at least one simulation."""
    with pytest.raises(ValueError, match="n_runs must be greater than zero"):
        run_monte_carlo(0, DebtFirstPolicy(), seed=1)


def test_aggregate_metrics_calculates_known_population_statistics() -> None:
    """Aggregate each metric from known Monte Carlo results."""
    results = (
        MonteCarloResult(2, 3.0, 0.25, 8.0),
        MonteCarloResult(4, 1.0, 0.75, 4.0),
    )

    metrics = aggregate_metrics(results)

    assert metrics["sprint_count"] == MetricSummary(3.0, 1.0, 2, 4)
    assert metrics["final_technical_debt"] == MetricSummary(2.0, 1.0, 1.0, 3.0)
    assert metrics["mean_remediation_fraction"] == MetricSummary(0.5, 0.25, 0.25, 0.75)
    assert metrics["final_backlog"] == MetricSummary(6.0, 2.0, 4.0, 8.0)


def test_monte_carlo_keeps_per_run_metrics_and_aggregates() -> None:
    """Store calculated metrics both per run and for the complete batch."""
    simulation = run_monte_carlo(
        2,
        DebtFirstPolicy(),
        seed=1,
        base_parameters=base_parameters(),
    )

    assert all(run.metrics.sprint_count == 3 for run in simulation.runs)
    assert simulation.metrics["sprint_count"].mean == 3.0


def test_monte_carlo_handles_runs_with_no_initial_work() -> None:
    """Return zero metrics when a run starts with no backlog or debt."""
    empty_parameters = ModelParameters(
        B0=0.0,
        D0=0.0,
        V0=4.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=3,
        s=1.0,
    )

    simulation = run_monte_carlo(
        1,
        DebtFirstPolicy(),
        seed=1,
        base_parameters=empty_parameters,
    )

    assert simulation.runs[0].metrics == MonteCarloResult(0, 0.0, 0.0, 0.0)
    assert simulation.summary.final_backlogs == (0.0,)
    assert simulation.summary.final_technical_debts == (0.0,)
