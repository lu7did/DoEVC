"""Tests for CSV exports."""

import csv
from dataclasses import replace
from pathlib import Path

from s004 import (
    MetricSummary,
    export_metrics_csv,
    export_sprint_states_csv,
    simulate_deterministic_sprints,
)
from tests.support import create_competing_parameters


def test_export_sprint_states_csv_writes_required_columns_and_rows(
    tmp_path: Path,
) -> None:
    """Export every sprint state with the documented column names."""
    states = simulate_deterministic_sprints(
        replace(create_competing_parameters(), D0=4.0, K=2),
        0.5,
    )
    filepath = tmp_path / "states.csv"

    export_sprint_states_csv(states, filepath)

    with filepath.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert rows[0] == {
        "sprint": "1",
        "B_k": "10.0",
        "D_k": "4.0",
        "V_k": "10.0",
        "u_k": "0.5",
        "N_k": "5.0",
        "R_k": "5.0",
    }
    assert len(rows) == 2


def test_export_metrics_csv_writes_readable_aggregate_metrics(tmp_path: Path) -> None:
    """Export aggregate metrics using standard CSV rows."""
    filepath = tmp_path / "metrics.csv"

    export_metrics_csv(
        {"final_backlog": MetricSummary(2.0, 1.0, 1.0, 3.0)},
        filepath,
    )

    with filepath.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert rows == [
        {
            "metric": "final_backlog",
            "mean": "2.0",
            "standard_deviation": "1.0",
            "minimum": "1.0",
            "maximum": "3.0",
        }
    ]
