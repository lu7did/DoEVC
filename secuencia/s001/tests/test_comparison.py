"""Tests for policy comparison tables in DoEVC s001."""

from types import SimpleNamespace

import pytest

from doevc_s001 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    EconomicObjectiveFunction,
    ModelParameters,
    MonteCarloPolicyComparisonRow,
    OptimalLocalPolicy,
    PolicyComparisonTable,
    ProportionalDebtPolicy,
    compare_policies,
    run_monte_carlo,
)
from doevc_s001 import comparison as comparison_module


def sample_parameters() -> ModelParameters:
    """Return a representative parameter set for comparison tests."""
    return ModelParameters(
        B0=4.0,
        D0=2.0,
        V0=3.0,
        alpha=0.2,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=3,
        s=1.0,
    )


def sample_objective() -> EconomicObjectiveFunction:
    """Return the reference economic objective for comparison tests."""
    return EconomicObjectiveFunction(
        delivered_value_weight=1.0,
        residual_debt_penalty_weight=1.0,
        sprint_penalty_weight=0.0,
    )


def sample_policies() -> dict[str, object]:
    """Return the policy set to compare across scenarios."""
    objective = sample_objective()
    return {
        "debt_first": DebtFirstPolicy(),
        "backlog_first": BacklogFirstPolicy(),
        "proportional": ProportionalDebtPolicy(),
        "optimal_local": OptimalLocalPolicy(objective=objective, step=0.25),
    }


def test_compare_policies_returns_deterministic_table_with_all_policies() -> None:
    """Return one deterministic row per evaluated policy."""
    table = compare_policies(
        sample_parameters(),
        sample_policies(),
        sample_objective(),
    )

    assert isinstance(table, PolicyComparisonTable)
    assert table.mode == "deterministic"
    assert {row.policy_name for row in table.rows} == {
        "debt_first",
        "backlog_first",
        "proportional",
        "optimal_local",
    }
    assert len({row.total_economic_value for row in table.rows}) > 1


def test_compare_policies_returns_monte_carlo_table_with_all_policies() -> None:
    """Return one Monte Carlo aggregate row per evaluated policy."""
    table = compare_policies(
        sample_parameters(),
        sample_policies(),
        sample_objective(),
        n_runs=3,
        seed=123,
    )

    assert table.mode == "monte_carlo"
    assert {row.policy_name for row in table.rows} == {
        "debt_first",
        "backlog_first",
        "proportional",
        "optimal_local",
    }
    assert all(isinstance(row, MonteCarloPolicyComparisonRow) for row in table.rows)
    assert all(row.n_runs == 3 for row in table.rows)
    assert len({row.final_backlog.mean for row in table.rows}) > 1


def test_compare_policies_uses_the_supplied_objective_in_monte_carlo_mode() -> None:
    """Recompute Monte Carlo economic values with the caller objective."""
    objective = EconomicObjectiveFunction(
        delivered_value_weight=0.0,
        residual_debt_penalty_weight=0.0,
        sprint_penalty_weight=1.0,
    )
    table = compare_policies(
        sample_parameters(),
        {"debt_first": DebtFirstPolicy()},
        objective,
        n_runs=3,
        seed=321,
    )
    baseline = run_monte_carlo(
        3,
        DebtFirstPolicy(),
        seed=321,
        base_parameters=sample_parameters(),
    )
    expected_values = tuple(
        objective(run.trajectory, run.sampled_parameters) for run in baseline.runs
    )

    row = table.rows[0]

    assert row.total_economic_value.mean == pytest.approx(sum(expected_values) / 3.0)


def test_compare_policies_rejects_empty_policy_sets() -> None:
    """Reject comparison requests without any policy to evaluate."""
    with pytest.raises(ValueError, match="must not be empty"):
        compare_policies(
            sample_parameters(),
            {},
            sample_objective(),
        )


def test_compare_policies_handles_deterministic_zero_work_scenarios() -> None:
    """Return zeroed deterministic metrics when the scenario starts completed."""
    parameters = ModelParameters(
        B0=0.0,
        D0=0.0,
        V0=3.0,
        alpha=0.2,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=3,
        s=1.0,
    )
    table = compare_policies(
        parameters,
        {"debt_first": DebtFirstPolicy()},
        sample_objective(),
    )

    row = table.rows[0]

    assert row.convergence_sprints == 0
    assert row.final_backlog == 0.0
    assert row.final_technical_debt == 0.0
    assert row.average_remediation_fraction == 0.0
    assert row.completed is True


def test_compare_policies_reports_missing_monte_carlo_economic_value() -> None:
    """Raise a clear error if Monte Carlo aggregation loses economic values."""

    def broken_aggregate_metrics(runs: tuple[object, ...]) -> object:
        """Return an invalid aggregate result for branch coverage."""
        del runs
        metric = SimpleNamespace(
            mean=0.0,
            standard_deviation=0.0,
            minimum=0.0,
            maximum=0.0,
            percentile_25=0.0,
            percentile_50=0.0,
            percentile_75=0.0,
        )
        return SimpleNamespace(
            n_runs=1,
            completed_runs=0,
            convergence_sprints=metric,
            final_backlog=metric,
            final_technical_debt=metric,
            average_remediation_fraction=metric,
            total_economic_value=None,
        )

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(
        comparison_module,
        "aggregate_metrics",
        broken_aggregate_metrics,
    )
    try:
        with pytest.raises(RuntimeError, match="economic value is missing"):
            compare_policies(
                sample_parameters(),
                {"debt_first": DebtFirstPolicy()},
                sample_objective(),
                n_runs=1,
                seed=11,
            )
    finally:
        monkeypatch.undo()
