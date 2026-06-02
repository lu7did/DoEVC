"""Tests for Monte Carlo execution and metrics in DoEVC s001."""

import csv
from dataclasses import dataclass, field

import pytest

from doevc_s001 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    MetricSummary,
    ModelParameters,
    MonteCarloAggregateResult,
    MonteCarloResult,
    MonteCarloRunResult,
    aggregate_metrics,
    export_monte_carlo_metrics_csv,
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
    assert all(0.0 <= run.average_remediation_fraction <= 1.0 for run in result.runs)
    assert all(1.0 <= run.sampled_parameters.s <= 1.4 for run in result.runs)
    assert all(0.0 <= run.sampled_parameters.gamma <= 0.05 for run in result.runs)
    assert all(0.0 <= run.sampled_parameters.theta <= 0.9 for run in result.runs)
    assert all(0.5 <= 1.0 - run.sampled_parameters.beta <= 0.9 for run in result.runs)
    assert all(0.2 <= run.sampled_parameters.lambda_ <= 1.0 for run in result.runs)
    assert isinstance(result.aggregate.final_backlog, MetricSummary)
    assert isinstance(result.aggregate, MonteCarloAggregateResult)


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


def test_aggregate_metrics_matches_known_run_values() -> None:
    """Aggregate known per-run metrics with expected summary statistics."""
    runs = (
        MonteCarloRunResult(
            run_index=1,
            sampled_parameters=sample_parameters(),
            trajectory=(),
            convergence_sprints=2,
            final_backlog=4.0,
            final_technical_debt=1.0,
            average_remediation_fraction=0.25,
            total_economic_value=10.0,
            completed=False,
        ),
        MonteCarloRunResult(
            run_index=2,
            sampled_parameters=sample_parameters(),
            trajectory=(),
            convergence_sprints=4,
            final_backlog=2.0,
            final_technical_debt=3.0,
            average_remediation_fraction=0.75,
            total_economic_value=20.0,
            completed=False,
        ),
    )

    aggregate = aggregate_metrics(runs)

    assert aggregate.n_runs == 2
    assert aggregate.completed_runs == 0
    assert aggregate.convergence_sprints.mean == 3.0
    assert aggregate.convergence_sprints.standard_deviation == 1.0
    assert aggregate.convergence_sprints.minimum == 2.0
    assert aggregate.convergence_sprints.maximum == 4.0
    assert aggregate.final_backlog.mean == 3.0
    assert aggregate.final_technical_debt.mean == 2.0
    assert aggregate.average_remediation_fraction.mean == 0.5
    assert aggregate.total_economic_value is not None
    assert aggregate.total_economic_value.mean == 15.0


def test_aggregate_metrics_rejects_empty_runs() -> None:
    """Reject aggregation requests without any run results."""
    with pytest.raises(ValueError, match="must not be empty"):
        aggregate_metrics(())


def test_export_monte_carlo_metrics_csv_writes_stable_columns(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """Export the run metrics with stable CSV column names."""
    result = run_monte_carlo(
        2,
        DebtFirstPolicy(),
        seed=44,
        base_parameters=sample_parameters(),
    )

    csv_path = export_monte_carlo_metrics_csv(
        result,
        tmp_path / "metrics.csv",
    )

    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = tuple(reader)

    assert reader.fieldnames == [
        "run_index",
        "convergence_sprints",
        "final_backlog",
        "final_technical_debt",
        "average_remediation_fraction",
        "total_economic_value",
        "completed",
    ]
    assert len(rows) == 2
