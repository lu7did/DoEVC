"""Tests for CSV export helpers in DoEVC s001."""

import csv

from doevc_s001 import (
    DebtFirstPolicy,
    ModelParameters,
    aggregate_metrics,
    export_metrics_csv,
    export_sprint_states_csv,
    run_monte_carlo,
    simulate_deterministic_sprints,
)


def sample_parameters() -> ModelParameters:
    """Return a representative parameter set for export tests."""
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
        K=3,
        s=1.0,
    )


def test_export_sprint_states_csv_writes_expected_columns_and_values(
    tmp_path: str,
) -> None:
    """Write one row per sprint with the documented state columns."""
    states = simulate_deterministic_sprints(sample_parameters(), DebtFirstPolicy())

    csv_path = export_sprint_states_csv(states, tmp_path / "states.csv")

    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = tuple(reader)

    assert reader.fieldnames == ["sprint", "B_k", "D_k", "V_k", "u_k", "N_k", "R_k"]
    assert len(rows) == len(states)
    assert rows[0]["sprint"] == "1"
    assert float(rows[0]["B_k"]) == states[0].backlog
    assert float(rows[0]["D_k"]) == states[0].technical_debt
    assert float(rows[0]["V_k"]) == states[0].effective_velocity
    assert float(rows[0]["u_k"]) == states[0].remediation_fraction
    assert float(rows[0]["N_k"]) == states[0].feature_capacity
    assert float(rows[0]["R_k"]) == states[0].remediation_capacity


def test_export_metrics_csv_writes_aggregate_metric_rows(tmp_path: str) -> None:
    """Write one row per aggregate Monte Carlo metric."""
    result = run_monte_carlo(
        2,
        DebtFirstPolicy(),
        seed=17,
        base_parameters=sample_parameters(),
    )

    csv_path = export_metrics_csv(result.aggregate, tmp_path / "metrics.csv")

    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = tuple(reader)

    assert reader.fieldnames == [
        "metric",
        "n_runs",
        "completed_runs",
        "mean",
        "standard_deviation",
        "minimum",
        "maximum",
        "percentile_25",
        "percentile_50",
        "percentile_75",
    ]
    assert [row["metric"] for row in rows] == [
        "convergence_sprints",
        "final_backlog",
        "final_technical_debt",
        "average_remediation_fraction",
        "total_economic_value",
    ]
    assert all(int(row["n_runs"]) == result.aggregate.n_runs for row in rows)


def test_export_metrics_csv_skips_missing_economic_value_row(tmp_path: str) -> None:
    """Omit the economic value row when the aggregate does not define it."""
    result = run_monte_carlo(
        1,
        DebtFirstPolicy(),
        seed=23,
        base_parameters=sample_parameters(),
    )
    metrics_without_economic_value = aggregate_metrics(
        tuple(
            run.__class__(
                run_index=run.run_index,
                sampled_parameters=run.sampled_parameters,
                trajectory=run.trajectory,
                convergence_sprints=run.convergence_sprints,
                final_backlog=run.final_backlog,
                final_technical_debt=run.final_technical_debt,
                average_remediation_fraction=run.average_remediation_fraction,
                total_economic_value=None,
                completed=run.completed,
            )
            for run in result.runs
        )
    )

    csv_path = export_metrics_csv(
        metrics_without_economic_value,
        tmp_path / "metrics-without-economic-value.csv",
    )

    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        rows = tuple(csv.DictReader(csv_file))

    assert [row["metric"] for row in rows] == [
        "convergence_sprints",
        "final_backlog",
        "final_technical_debt",
        "average_remediation_fraction",
    ]
