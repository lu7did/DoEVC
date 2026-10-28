"""Tests for Monte Carlo simulations."""

import pytest

from s004 import DebtFirstPolicy, ModelParameters, run_monte_carlo


def create_base_parameters() -> ModelParameters:
    """Return compact deterministic parameters for Monte Carlo tests."""
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
    )


def test_monte_carlo_is_reproducible_with_a_fixed_seed() -> None:
    """A fixed seed produces equal individual and aggregate results."""
    first = run_monte_carlo(
        3,
        DebtFirstPolicy(),
        seed=1234,
        base_parameters=create_base_parameters(),
    )
    second = run_monte_carlo(
        3,
        DebtFirstPolicy(),
        seed=1234,
        base_parameters=create_base_parameters(),
    )

    assert first == second


def test_monte_carlo_executes_requested_number_of_runs() -> None:
    """One result and aggregate entry are returned per requested run."""
    result = run_monte_carlo(
        4,
        DebtFirstPolicy(),
        seed=7,
        base_parameters=create_base_parameters(),
    )

    assert len(result.runs) == 4
    assert result.summary.run_count == 4
    assert len(result.summary.final_backlogs) == 4
    assert len(result.summary.final_technical_debts) == 4
    assert all(run.trajectory[0].remediation_fraction == 1.0 for run in result.runs)


def test_monte_carlo_rejects_non_positive_run_counts() -> None:
    """At least one simulation run is required."""
    with pytest.raises(ValueError, match="n_runs must be greater than zero"):
        run_monte_carlo(0, DebtFirstPolicy(), seed=1)
