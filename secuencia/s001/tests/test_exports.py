"""Tests for CSV export helpers in DoEVC s001."""

import csv
import json

import pytest

from doevc_s001 import (
    DebtFirstPolicy,
    ModelParameters,
    aggregate_metrics,
    export_metrics_csv,
    export_sprint_states_csv,
    load_and_run,
    run_monte_carlo,
    save_scenario,
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


def test_save_scenario_writes_expected_json_structure(tmp_path: str) -> None:
    """Persist a scenario as standard JSON with the expected top-level fields."""
    json_path = save_scenario(
        sample_parameters(),
        "DebtFirstPolicy",
        123,
        tmp_path / "scenario.json",
    )

    with json_path.open(encoding="utf-8") as json_file:
        payload = json.load(json_file)

    assert payload == {
        "parameters": sample_parameters().to_dict(),
        "policy_name": "DebtFirstPolicy",
        "seed": 123,
    }


def test_save_scenario_serializes_binary_seeds_as_json_safe_data(tmp_path: str) -> None:
    """Convert binary seeds to structured JSON data so the file stays loadable."""
    json_path = save_scenario(
        sample_parameters(),
        "DebtFirstPolicy",
        b"\x01\x02\x03",
        tmp_path / "scenario-bytes.json",
    )

    with json_path.open(encoding="utf-8") as json_file:
        payload = json.load(json_file)

    assert payload["seed"] == {
        "type": "bytes",
        "value": [1, 2, 3],
    }


def test_load_and_run_reproduces_a_saved_scenario_round_trip(tmp_path: str) -> None:
    """Load a saved scenario and reproduce the original deterministic trajectory."""
    parameters = sample_parameters()
    original = simulate_deterministic_sprints(parameters, DebtFirstPolicy())
    json_path = save_scenario(
        parameters,
        "DebtFirstPolicy",
        123,
        tmp_path / "round-trip-scenario.json",
    )

    loaded = load_and_run(json_path)

    assert loaded == original


@pytest.mark.parametrize(
    ("seed", "expected_payload"),
    [
        (
            b"\x01\x02\x03",
            {
                "type": "bytes",
                "value": [1, 2, 3],
            },
        ),
        (
            bytearray(b"\x04\x05\x06"),
            {
                "type": "bytearray",
                "value": [4, 5, 6],
            },
        ),
    ],
)
def test_load_and_run_accepts_serialized_binary_seeds(
    tmp_path: str,
    seed: bytes | bytearray,
    expected_payload: dict[str, object],
) -> None:
    """Accept serialized bytes and bytearray seeds when replaying a scenario."""
    parameters = sample_parameters()
    original = simulate_deterministic_sprints(parameters, DebtFirstPolicy())
    json_path = save_scenario(
        parameters,
        "DebtFirstPolicy",
        seed,
        tmp_path / "binary-seed-scenario.json",
    )

    with json_path.open(encoding="utf-8") as json_file:
        payload = json.load(json_file)

    assert payload["seed"] == expected_payload
    assert load_and_run(json_path) == original


@pytest.mark.parametrize(
    ("seed_payload", "message"),
    [
        (
            {
                "type": 7,
                "value": [1, 2, 3],
            },
            "serialized seed type must be a string",
        ),
        (
            {
                "type": "bytes",
                "value": "123",
            },
            "serialized seed values must be an integer list",
        ),
        (
            {
                "type": "bytes",
                "value": [1, "2", 3],
            },
            "serialized seed values must be an integer list",
        ),
        (
            {
                "type": "memoryview",
                "value": [1, 2, 3],
            },
            "serialized seed type is not supported",
        ),
    ],
)
def test_load_and_run_rejects_invalid_serialized_seeds(
    tmp_path: str,
    seed_payload: dict[str, object],
    message: str,
) -> None:
    """Raise a clear error when a saved scenario contains an invalid serialized seed."""
    json_path = save_scenario(
        sample_parameters(),
        "DebtFirstPolicy",
        123,
        tmp_path / "invalid-seed-scenario.json",
    )

    with json_path.open(encoding="utf-8") as json_file:
        payload = json.load(json_file)

    payload["seed"] = seed_payload

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(payload, json_file)

    with pytest.raises(ValueError, match=message):
        load_and_run(json_path)


def test_load_and_run_rejects_unknown_policy_names(tmp_path: str) -> None:
    """Raise a clear error when the scenario names an unsupported policy."""
    json_path = save_scenario(
        sample_parameters(),
        "UnknownPolicy",
        123,
        tmp_path / "unknown-policy.json",
    )

    with json_path.open(encoding="utf-8") as json_file:
        payload = json.load(json_file)

    payload["policy_name"] = "UnknownPolicy"

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(payload, json_file)

    with pytest.raises(ValueError, match="is not registered"):
        load_and_run(json_path)
