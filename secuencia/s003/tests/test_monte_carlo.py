"""Regression tests for Monte Carlo executions in s003."""

from doevc_s003 import DebtFirstPolicy, run_monte_carlo


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
