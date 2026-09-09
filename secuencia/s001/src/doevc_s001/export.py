"""CSV export helpers for simulation states and Monte Carlo metrics."""

import csv
from collections.abc import Mapping, Sequence
from pathlib import Path

from .monte_carlo import MetricSummary
from .sprint import SprintState


def export_sprint_states_csv(
    states: Sequence[SprintState],
    filepath: str | Path,
) -> None:
    """Write one CSV row per sprint state."""
    with Path(filepath).open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=("sprint", "B_k", "D_k", "V_k", "u_k", "N_k", "R_k"),
        )
        writer.writeheader()
        for sprint, state in enumerate(states, start=1):
            writer.writerow(
                {
                    "sprint": sprint,
                    "B_k": state.backlog,
                    "D_k": state.technical_debt,
                    "V_k": state.effective_velocity,
                    "u_k": state.remediation_fraction,
                    "N_k": state.feature_capacity,
                    "R_k": state.remediation_capacity,
                }
            )


def export_metrics_csv(
    metrics: Mapping[str, MetricSummary],
    filepath: str | Path,
) -> None:
    """Write aggregate Monte Carlo metrics to a CSV file."""
    with Path(filepath).open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=(
                "metric",
                "mean",
                "standard_deviation",
                "minimum",
                "maximum",
            ),
        )
        writer.writeheader()
        for metric, summary in metrics.items():
            writer.writerow(
                {
                    "metric": metric,
                    "mean": summary.mean,
                    "standard_deviation": summary.standard_deviation,
                    "minimum": summary.minimum,
                    "maximum": summary.maximum,
                }
            )
