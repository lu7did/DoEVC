"""Portable JSON scenario serialization."""

import json
from collections.abc import Callable
from numbers import Real
from pathlib import Path
from typing import cast

from .models import ModelParameters
from .policies import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    Policy,
    ProportionalPolicy,
)
from .simulation import simulate_sprints
from .sprint import SprintState

POLICY_REGISTRY: dict[str, Callable[[], Policy]] = {
    "BacklogFirstPolicy": BacklogFirstPolicy,
    "DebtFirstPolicy": DebtFirstPolicy,
    "ProportionalPolicy": ProportionalPolicy,
}
_PARAMETER_FIELDS = frozenset(
    {"B0", "D0", "V0", "alpha", "beta", "gamma", "theta", "lambda_", "rho", "K"}
)


def _as_string_mapping(value: object) -> dict[str, object] | None:
    """Normalize a JSON object to its string-keyed mapping representation."""
    if not isinstance(value, dict):
        return None
    return cast(dict[str, object], value)


def _require_real(parameters: dict[str, object], field_name: str) -> float:
    """Extract one JSON real-valued model parameter."""
    value = parameters[field_name]
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"scenario parameter {field_name} must be a real number.")
    return float(value)


def _load_parameters(value: object) -> ModelParameters:
    """Validate and reconstruct the complete serialized parameter model."""
    parameters = _as_string_mapping(value)
    if parameters is None or set(parameters) != set(_PARAMETER_FIELDS):
        raise ValueError("scenario parameters do not match ModelParameters.")
    sprint_limit = parameters["K"]
    if isinstance(sprint_limit, bool) or not isinstance(sprint_limit, int):
        raise ValueError("scenario parameter K must be an integer.")
    return ModelParameters(
        B0=_require_real(parameters, "B0"),
        D0=_require_real(parameters, "D0"),
        V0=_require_real(parameters, "V0"),
        alpha=_require_real(parameters, "alpha"),
        beta=_require_real(parameters, "beta"),
        gamma=_require_real(parameters, "gamma"),
        theta=_require_real(parameters, "theta"),
        lambda_=_require_real(parameters, "lambda_"),
        rho=_require_real(parameters, "rho"),
        K=sprint_limit,
    )


def save_scenario(
    params: ModelParameters,
    policy_name: str,
    seed: int | None,
    filepath: str | Path,
) -> None:
    """Save complete reproducibility inputs as a JSON scenario document."""
    if not policy_name:
        raise ValueError("policy_name must not be empty.")
    scenario = {
        "parameters": params.to_dict(),
        "policy_name": policy_name,
        "seed": seed,
    }
    with Path(filepath).open("w", encoding="utf-8") as output:
        json.dump(scenario, output, indent=2, sort_keys=True)


def load_and_run(filepath: str | Path) -> list[SprintState]:
    """Load a saved scenario and reproduce its deterministic trajectory."""
    with Path(filepath).open(encoding="utf-8") as input_file:
        serialized_scenario: object = json.load(input_file)
    scenario = _as_string_mapping(serialized_scenario)
    if scenario is None:
        raise ValueError("scenario must be a JSON object.")

    parameters_data: object = scenario.get("parameters")
    policy_name = scenario.get("policy_name")
    seed = scenario.get("seed")
    if not isinstance(policy_name, str):
        raise ValueError("scenario policy_name must be a string.")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise ValueError("scenario seed must be an integer or null.")

    policy_factory = POLICY_REGISTRY.get(policy_name)
    if policy_factory is None:
        raise ValueError(f"unsupported policy_name: {policy_name}.")
    parameters = _load_parameters(parameters_data)
    return simulate_sprints(parameters, policy_factory())
