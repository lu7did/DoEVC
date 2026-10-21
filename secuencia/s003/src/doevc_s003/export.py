"""CSV exports for simulation trajectories and aggregate metrics."""

import csv
from collections.abc import Sequence
from pathlib import Path

from .monte_carlo import AggregateMetrics, MetricSummary
from .sprint import SprintState


def export_sprint_states_csv(
    states: Sequence[SprintState], filepath: str | Path
) -> None:
    """Write one CSV row per sprint state using the model's standard symbols."""
    with Path(filepath).open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(
            output,
            fieldnames=["sprint", "B_k", "D_k", "V_k", "u_k", "N_k", "R_k"],
        )
        writer.writeheader()
        for sprint, state in enumerate(states):
            writer.writerow(
                {
                    "sprint": sprint,
                    "B_k": state.backlog,
                    "D_k": state.debt,
                    "V_k": state.velocity,
                    "u_k": state.allocation,
                    "N_k": state.delivery_capacity,
                    "R_k": state.remediation_capacity,
                }
            )


def _metric_rows(metrics: AggregateMetrics) -> tuple[tuple[str, MetricSummary], ...]:
    """Return named summaries in the stable CSV row order."""
    return (
        ("total_sprints", metrics.total_sprints),
        ("final_debt", metrics.final_debt),
        ("average_allocation", metrics.average_allocation),
        ("final_backlog", metrics.final_backlog),
    )


def export_metrics_csv(metrics: AggregateMetrics, filepath: str | Path) -> None:
    """Write C3 aggregate metrics to a standard, analysis-ready CSV file."""
    with Path(filepath).open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(
            output,
            fieldnames=["metric", "mean", "standard_deviation", "minimum", "maximum"],
        )
        writer.writeheader()
        for name, summary in _metric_rows(metrics):
            writer.writerow(
                {
                    "metric": name,
                    "mean": summary.mean,
                    "standard_deviation": summary.standard_deviation,
                    "minimum": summary.minimum,
                    "maximum": summary.maximum,
                }
            )
