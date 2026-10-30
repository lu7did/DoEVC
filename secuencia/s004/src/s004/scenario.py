"""Scenario persistence helpers."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import cast

from .models import ModelParameters
from .policies import BacklogFirstPolicy, DebtFirstPolicy, Policy, ProportionalPolicy
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

_POLICY_REGISTRY: dict[str, Callable[[], Policy]] = {
    "BacklogFirstPolicy": BacklogFirstPolicy,
    "DebtFirstPolicy": DebtFirstPolicy,
    "ProportionalPolicy": ProportionalPolicy,
}


def save_scenario(
    params: ModelParameters,
    policy_name: str,
    seed: int | None,
    filepath: str | Path,
) -> None:
    """Serialize a reproducible simulation scenario to JSON."""
    scenario = {
        "parameters": params.to_dict(),
        "policy_name": policy_name,
        "seed": seed,
    }
    with Path(filepath).open("w", encoding="utf-8") as json_file:
        json.dump(scenario, json_file, indent=2, sort_keys=True)
        json_file.write("\n")


def load_and_run(filepath: str | Path) -> tuple[SprintState, ...]:
    """Load a saved scenario and reproduce its deterministic trajectory."""
    with Path(filepath).open(encoding="utf-8") as json_file:
        scenario: object = json.load(json_file)

    scenario_data = _normalize_json_object(scenario, "scenario")
    parameters = _load_parameters(scenario_data.get("parameters"))
    policy = _load_policy(scenario_data.get("policy_name"))
    _load_seed(scenario_data.get("seed"))
    return simulate_deterministic_sprints(parameters, policy)


def _load_parameters(data: object) -> ModelParameters:
    """Reconstruct model parameters from a JSON object."""
    values = _normalize_json_object(data, "scenario parameters")
    return ModelParameters(
        B0=_load_float(values, "B0"),
        D0=_load_float(values, "D0"),
        V0=_load_float(values, "V0"),
        alpha=_load_float(values, "alpha"),
        beta=_load_float(values, "beta"),
        gamma=_load_float(values, "gamma"),
        theta=_load_float(values, "theta"),
        lambda_=_load_float(values, "lambda_"),
        rho=_load_float(values, "rho"),
        K=_load_integer(values, "K"),
        s=_load_float(values, "s"),
    )


def _normalize_json_object(data: object, name: str) -> dict[str, object]:
    """Validate and normalize an object decoded from JSON."""
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object.")

    normalized: dict[str, object] = {}
    for key, value in cast(dict[object, object], data).items():
        if not isinstance(key, str):
            raise ValueError(f"{name} keys must be strings.")
        normalized[key] = value
    return normalized


def _load_float(values: dict[str, object], name: str) -> float:
    """Load one numeric JSON field as a float."""
    value = values.get(name)
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"scenario parameter {name} must be numeric.")
    return float(value)


def _load_integer(values: dict[str, object], name: str) -> int:
    """Load one integer JSON field."""
    value = values.get(name)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"scenario parameter {name} must be an integer.")
    return value


def _load_policy(policy_name: object) -> Policy:
    """Instantiate a registered policy from its saved class name."""
    if not isinstance(policy_name, str):
        raise ValueError("scenario policy_name must be a string.")
    try:
        policy_factory = _POLICY_REGISTRY[policy_name]
    except KeyError as error:
        raise ValueError(f"unknown policy: {policy_name}.") from error
    return policy_factory()


def _load_seed(seed: object) -> int | None:
    """Validate the seed retained for experiment traceability."""
    if seed is None or (isinstance(seed, int) and not isinstance(seed, bool)):
        return seed
    raise ValueError("scenario seed must be an integer or null.")
