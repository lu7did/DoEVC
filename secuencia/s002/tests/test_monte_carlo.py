"""Regression tests for Monte Carlo simulation execution."""

from doevc_s002 import DebtFirstPolicy, run_monte_carlo


def test_monte_carlo_runs_exactly_the_requested_number_of_simulations() -> None:
    """Preserve every individual run and expose its aggregate count."""
    result = run_monte_carlo(3, DebtFirstPolicy(), seed=7)

    assert result.n_runs == 3
    assert len(result.runs) == 3


def test_monte_carlo_is_reproducible_for_a_fixed_seed() -> None:
    """Return equal parameters and trajectories for equal seeds."""
    assert run_monte_carlo(2, DebtFirstPolicy(), 42) == run_monte_carlo(
        2, DebtFirstPolicy(), 42
    )
