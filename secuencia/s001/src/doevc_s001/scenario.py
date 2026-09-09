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
    params = _load_parameters(scenario_data.get("parameters"))
    policy = _load_policy(scenario_data.get("policy_name"))
    _load_seed(scenario_data.get("seed"))
    return simulate_deterministic_sprints(params, policy)


def _load_parameters(data: object) -> ModelParameters:
    """Reconstruct model parameters from a JSON object."""
    parameters_data = _normalize_json_object(data, "scenario parameters")

    return ModelParameters(
        B0=_load_float(parameters_data, "B0"),
        D0=_load_float(parameters_data, "D0"),
        V0=_load_float(parameters_data, "V0"),
        alpha=_load_float(parameters_data, "alpha"),
        beta=_load_float(parameters_data, "beta"),
        gamma=_load_float(parameters_data, "gamma"),
        theta=_load_float(parameters_data, "theta"),
        lambda_=_load_float(parameters_data, "lambda_"),
        rho=_load_float(parameters_data, "rho"),
        K=_load_integer(parameters_data, "K"),
        s=_load_float(parameters_data, "s"),
    )


def _normalize_json_object(data: object, name: str) -> dict[str, object]:
    """Validate and normalize an object decoded from JSON."""
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be a JSON object.")

    raw_data = cast(dict[object, object], data)
    normalized: dict[str, object] = {}
    for key, value in raw_data.items():
        if not isinstance(key, str):
            raise ValueError(f"{name} keys must be strings.")
        normalized[key] = value
    return normalized


def _load_float(data: dict[str, object], name: str) -> float:
    """Load one numeric JSON field as a float."""
    value = data.get(name)
    if not isinstance(value, int | float):
        raise ValueError(f"scenario parameter {name} must be numeric.")
    return float(value)


def _load_integer(data: dict[str, object], name: str) -> int:
    """Load one integer JSON field."""
    value = data.get(name)
    if not isinstance(value, int):
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
    if seed is None or isinstance(seed, int):
        return seed
    raise ValueError("scenario seed must be an integer or null.")
