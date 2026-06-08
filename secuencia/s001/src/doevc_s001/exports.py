"""CSV and JSON helpers for reproducible DoEVC experiments."""

from __future__ import annotations

import csv
import json
from collections.abc import Callable
from os import PathLike
from pathlib import Path
from typing import TypeGuard, cast

from .models import ModelParameters
from .montecarlo import MonteCarloAggregateResult
from .optimization import EconomicObjectiveFunction, OptimalLocalPolicy
from .policies import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    Policy,
    ProportionalDebtPolicy,
)
from .sampling import RandomSeed
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

type PolicyFactory = Callable[[], Policy]

_POLICY_REGISTRY: dict[str, PolicyFactory] = {
    "BacklogFirstPolicy": BacklogFirstPolicy,
    "DebtFirstPolicy": DebtFirstPolicy,
    "OptimalLocalPolicy": lambda: OptimalLocalPolicy(
        objective=EconomicObjectiveFunction()
    ),
    "ProportionalDebtPolicy": ProportionalDebtPolicy,
}


def _serialize_seed(seed: RandomSeed) -> int | float | str | None | dict[str, object]:
    """Serialize supported seed types to JSON-compatible values."""
    if isinstance(seed, (bytes, bytearray)):
        return {
            "type": type(seed).__name__,
            "value": list(seed),
        }
    return seed


def _deserialize_seed(
    seed: int | float | str | None | dict[str, object],
) -> RandomSeed:
    """Deserialize JSON-compatible seed data to the original supported type."""
    if isinstance(seed, dict):
        seed_type = seed.get("type")
        values = seed.get("value")
        if not isinstance(seed_type, str):
            raise ValueError("serialized seed type must be a string.")
        if not _is_integer_list(values):
            raise ValueError("serialized seed values must be an integer list.")
        integer_values = values
        if seed_type == "bytes":
            return bytes(integer_values)
        if seed_type == "bytearray":
            return bytearray(integer_values)
        raise ValueError("serialized seed type is not supported.")
    return seed


def _is_integer_list(value: object) -> TypeGuard[list[int]]:
    """Return whether a JSON value is a list containing only integers."""
    if not isinstance(value, list):
        return False
    return all(isinstance(item, int) for item in cast(list[object], value))


def export_sprint_states_csv(
    states: tuple[SprintState, ...],
    destination: str | PathLike[str],
) -> Path:
    """Export one CSV row per sprint state using the documented column names."""
    destination_path = Path(destination)
    fieldnames = ("sprint", "B_k", "D_k", "V_k", "u_k", "N_k", "R_k")

    with destination_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for sprint_number, state in enumerate(states, start=1):
            writer.writerow(
                {
                    "sprint": sprint_number,
                    "B_k": state.backlog,
                    "D_k": state.technical_debt,
                    "V_k": state.effective_velocity,
                    "u_k": state.remediation_fraction,
                    "N_k": state.feature_capacity,
                    "R_k": state.remediation_capacity,
                }
            )

    return destination_path


def export_metrics_csv(
    metrics: MonteCarloAggregateResult,
    destination: str | PathLike[str],
) -> Path:
    """Export aggregate Monte Carlo metric summaries to a CSV table."""
    destination_path = Path(destination)
    fieldnames = (
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
    )
    metric_rows = {
        "convergence_sprints": metrics.convergence_sprints,
        "final_backlog": metrics.final_backlog,
        "final_technical_debt": metrics.final_technical_debt,
        "average_remediation_fraction": metrics.average_remediation_fraction,
    }
    if metrics.total_economic_value is not None:
        metric_rows["total_economic_value"] = metrics.total_economic_value

    with destination_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for metric_name, summary in metric_rows.items():
            writer.writerow(
                {
                    "metric": metric_name,
                    "n_runs": metrics.n_runs,
                    "completed_runs": metrics.completed_runs,
                    "mean": summary.mean,
                    "standard_deviation": summary.standard_deviation,
                    "minimum": summary.minimum,
                    "maximum": summary.maximum,
                    "percentile_25": summary.percentile_25,
                    "percentile_50": summary.percentile_50,
                    "percentile_75": summary.percentile_75,
                }
            )

    return destination_path


def save_scenario(
    params: ModelParameters,
    policy_name: str,
    seed: RandomSeed,
    destination: str | PathLike[str],
) -> Path:
    """Save a reproducible experiment scenario to a JSON file."""
    destination_path = Path(destination)
    scenario = {
        "parameters": params.to_dict(),
        "policy_name": policy_name,
        "seed": _serialize_seed(seed),
    }

    with destination_path.open("w", encoding="utf-8") as json_file:
        json.dump(scenario, json_file, indent=2, sort_keys=True)

    return destination_path


def load_and_run(destination: str | PathLike[str]) -> tuple[SprintState, ...]:
    """Load a saved scenario JSON and execute the deterministic simulation."""
    destination_path = Path(destination)
    with destination_path.open(encoding="utf-8") as json_file:
        scenario = json.load(json_file)

    policy_name = scenario["policy_name"]
    try:
        policy = _POLICY_REGISTRY[policy_name]()
    except KeyError as error:
        raise ValueError(f"policy {policy_name!r} is not registered.") from error

    parameters = ModelParameters(**scenario["parameters"])
    _ = _deserialize_seed(scenario["seed"])
    return simulate_deterministic_sprints(parameters, policy)
