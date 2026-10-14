"""CSV exports for simulation trajectories and aggregate metrics."""

import csv
from collections.abc import Iterable, Mapping
from pathlib import Path

from .sprint import SprintState


def export_sprint_states_csv(
    states: Iterable[SprintState], filepath: str | Path
) -> None:
    """Write one deterministic sprint state per CSV row."""
    with Path(filepath).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=["sprint", "B_k", "D_k", "V_k", "u_k", "N_k", "R_k"]
        )
        writer.writeheader()
        for sprint, state in enumerate(states, start=1):
            writer.writerow(
                {
                    "sprint": sprint,
                    "B_k": state.backlog,
                    "D_k": state.debt,
                    "V_k": state.velocity,
                    "u_k": state.remediation_fraction,
                    "N_k": state.feature_capacity,
                    "R_k": state.remediation_capacity,
                }
            )


def export_metrics_csv(
    metrics: Mapping[str, Mapping[str, float]], filepath: str | Path
) -> None:
    """Write Monte Carlo aggregate metrics as a standard CSV table."""
    with Path(filepath).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=["metric", "mean", "stddev", "min", "max"]
        )
        writer.writeheader()
        for name, values in metrics.items():
            writer.writerow({"metric": name, **values})
