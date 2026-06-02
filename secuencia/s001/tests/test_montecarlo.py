"""Tests for Monte Carlo execution in DoEVC s001."""

from dataclasses import dataclass, field

import pytest

from doevc_s001 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    ModelParameters,
    MonteCarloResult,
    run_monte_carlo,
)


def sample_parameters(*, k: int = 4) -> ModelParameters:
    """Return a representative base parameter set for Monte Carlo tests."""
    return ModelParameters(
        B0=8.0,
        D0=4.0,
        V0=4.0,
        alpha=0.0,
        beta=0.2,
        gamma=0.01,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=k,
        s=1.0,
    )


def test_run_monte_carlo_reproduces_results_with_same_seed() -> None:
    """Return the same runs and aggregates for the same seed."""
    first = run_monte_carlo(
        4,
        DebtFirstPolicy(),
        seed=1234,
        base_parameters=sample_parameters(),
    )
    second = run_monte_carlo(
        4,
        DebtFirstPolicy(),
        seed=1234,
        base_parameters=sample_parameters(),
    )

    assert first == second


def test_run_monte_carlo_returns_individual_and_aggregate_results() -> None:
    """Expose both per-run outputs and aggregate summaries."""
    result = run_monte_carlo(
        3,
        DebtFirstPolicy(),
        seed=77,
        base_parameters=sample_parameters(),
    )

    assert isinstance(result, MonteCarloResult)
    assert len(result.runs) == 3
    assert result.aggregate.n_runs == 3
    assert result.aggregate.completed_runs <= 3
    assert all(run.run_index >= 1 for run in result.runs)
    assert all(1.0 <= run.sampled_parameters.s <= 1.4 for run in result.runs)
    assert all(0.0 <= run.sampled_parameters.gamma <= 0.05 for run in result.runs)
    assert all(0.0 <= run.sampled_parameters.theta <= 0.9 for run in result.runs)
    assert all(0.5 <= 1.0 - run.sampled_parameters.beta <= 0.9 for run in result.runs)
    assert all(0.2 <= run.sampled_parameters.lambda_ <= 1.0 for run in result.runs)


@dataclass(slots=True)
class CountingPolicy:
    """Count how many times the simulation requests a remediation decision."""

    calls: int = 0
    seen_backlogs: list[float] = field(default_factory=list)

    def decide_u(self, state: object, params: object) -> float:
        """Record the call and return no remediation."""
        del params
        self.calls += 1
        self.seen_backlogs.append(state.backlog)
        return 0.0


def test_run_monte_carlo_executes_exactly_n_runs() -> None:
    """Run exactly the requested number of simulations."""
    policy = CountingPolicy()
    result = run_monte_carlo(
        5,
        policy,
        seed=2025,
        base_parameters=sample_parameters(k=1),
    )

    assert len(result.runs) == 5
    assert policy.calls == 5
    assert result.aggregate.n_runs == 5


def test_run_monte_carlo_accepts_selectable_policies() -> None:
    """Allow swapping policies without changing the Monte Carlo engine."""
    debt_first = run_monte_carlo(
        2,
        DebtFirstPolicy(),
        seed=12,
        base_parameters=sample_parameters(),
    )
    backlog_first = run_monte_carlo(
        2,
        BacklogFirstPolicy(),
        seed=12,
        base_parameters=sample_parameters(),
    )

    assert debt_first != backlog_first


def test_run_monte_carlo_rejects_non_positive_run_count() -> None:
    """Reject an invalid number of Monte Carlo runs."""
    with pytest.raises(ValueError, match="greater than zero"):
        run_monte_carlo(
            0,
            DebtFirstPolicy(),
            seed=10,
            base_parameters=sample_parameters(),
        )
