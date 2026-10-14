"""Regression tests for CSV exports."""

import csv

from doevc_s002 import (
    ModelParameters,
    export_metrics_csv,
    export_sprint_states_csv,
    simulate_deterministic_sprints,
)


def test_export_sprint_states_csv_writes_required_columns(tmp_path: object) -> None:
    """Export trajectory rows readable by the standard CSV module."""
    filepath = tmp_path / "states.csv"  # type: ignore[operator]
    states = simulate_deterministic_sprints(
        ModelParameters(10, 0, 10, 0, 0, 0, 0, 0, 0, 1), 0
    )

    export_sprint_states_csv(states, filepath)

    with filepath.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert rows[0]["sprint"] == "1"
    assert set(rows[0]) == {"sprint", "B_k", "D_k", "V_k", "u_k", "N_k", "R_k"}


def test_export_metrics_csv_writes_aggregate_rows(tmp_path: object) -> None:
    """Export aggregate metric names and statistics as CSV rows."""
    filepath = tmp_path / "metrics.csv"  # type: ignore[operator]

    export_metrics_csv(
        {"sprints": {"mean": 2, "stddev": 0, "min": 2, "max": 2}}, filepath
    )

    with filepath.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert rows == [
        {"metric": "sprints", "mean": "2", "stddev": "0", "min": "2", "max": "2"}
    ]
