"""Regression tests for Monte Carlo executions in s003."""

from doevc_s003 import (
    DebtFirstPolicy,
    ModelParameters,
    MonteCarloRun,
    SprintState,
    aggregate_metrics,
    run_monte_carlo,
)


def test_monte_carlo_is_reproducible_with_the_same_seed() -> None:
    """Return identical individual and aggregated results for an equal seed."""
    policy = DebtFirstPolicy()

    assert run_monte_carlo(3, policy, seed=42) == run_monte_carlo(3, policy, seed=42)


def test_monte_carlo_executes_exactly_the_requested_number_of_runs() -> None:
    """Create one individual result per requested Monte Carlo execution."""
    result = run_monte_carlo(4, DebtFirstPolicy(), seed=7)

    assert len(result.runs) == 4
    assert result.mean_final_backlog is not None
    assert result.mean_final_debt is not None


def test_monte_carlo_returns_empty_aggregates_for_zero_runs() -> None:
    """Represent an explicitly empty experiment without a false average."""
    result = run_monte_carlo(0, DebtFirstPolicy(), seed=1)

    assert result.runs == ()
    assert result.mean_final_backlog is None
    assert result.mean_final_debt is None


def test_aggregate_metrics_summarizes_known_individual_runs() -> None:
    """Calculate population statistics across all required output metrics."""
    parameters = ModelParameters(10, 4, 5, 0, 0, 0, 0, 0, 0, 3)
    runs = (
        MonteCarloRun(
            parameters,
            (
                SprintState(10, 4, 0.2, 5, 1, 4, 7, 3),
                SprintState(7, 3, 0.4, 5, 2, 3, 0, 1),
            ),
        ),
        MonteCarloRun(
            parameters,
            (SprintState(10, 4, 0.6, 5, 3, 2, 2, 5),),
        ),
    )

    metrics = aggregate_metrics(runs)

    assert metrics.total_sprints.mean == 1.5
    assert metrics.total_sprints.standard_deviation == 0.5
    assert metrics.total_sprints.minimum == 1
    assert metrics.total_sprints.maximum == 2
    assert metrics.final_debt.mean == 3
    assert metrics.final_debt.standard_deviation == 2
    assert metrics.final_debt.minimum == 1
    assert metrics.final_debt.maximum == 5
    assert metrics.average_allocation.mean == 0.45
    assert metrics.final_backlog.mean == 1
