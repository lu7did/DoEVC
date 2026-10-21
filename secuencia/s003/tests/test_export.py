"""Regression tests for CSV exports in s003."""

import csv
from pathlib import Path

from doevc_s003 import (
    AggregateMetrics,
    MetricSummary,
    SprintState,
    export_metrics_csv,
    export_sprint_states_csv,
)


def test_sprint_state_export_writes_required_columns_and_rows(tmp_path: Path) -> None:
    """Create a readable CSV row with the state symbols for each sprint."""
    path = tmp_path / "states.csv"
    states = [SprintState(10, 4, 0.25, 8, 2, 6, 4, 2)]

    export_sprint_states_csv(states, path)

    with path.open(encoding="utf-8", newline="") as output:
        rows = list(csv.DictReader(output))
    assert rows == [
        {
            "sprint": "0",
            "B_k": "10",
            "D_k": "4",
            "V_k": "8",
            "u_k": "0.25",
            "N_k": "6",
            "R_k": "2",
        }
    ]


def test_metrics_export_writes_all_c3_summaries(tmp_path: Path) -> None:
    """Create standard CSV rows for every aggregate output metric."""
    path = tmp_path / "metrics.csv"
    summary = MetricSummary(2, 0.5, 1, 3)
    metrics = AggregateMetrics(summary, summary, summary, summary)

    export_metrics_csv(metrics, path)

    with path.open(encoding="utf-8", newline="") as output:
        rows = list(csv.DictReader(output))
    assert [row["metric"] for row in rows] == [
        "total_sprints",
        "final_debt",
        "average_allocation",
        "final_backlog",
    ]
    assert rows[0]["mean"] == "2"
    assert rows[0]["standard_deviation"] == "0.5"
