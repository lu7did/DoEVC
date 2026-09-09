"""Tests for Monte Carlo simulation runs."""

import pytest

from doevc_s001 import (
    DebtFirstPolicy,
    ModelParameters,
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
