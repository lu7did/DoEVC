"""Persistence of reproducible simulation scenarios."""

import json
from pathlib import Path

from .models import ModelParameters
from .policies import BacklogFirstPolicy, DebtFirstPolicy, Policy, ProportionalPolicy
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

POLICY_REGISTRY: dict[str, type[Policy]] = {
    "DebtFirstPolicy": DebtFirstPolicy,
    "BacklogFirstPolicy": BacklogFirstPolicy,
    "ProportionalPolicy": ProportionalPolicy,
}


def save_scenario(
    parameters: ModelParameters,
    policy_name: str,
    seed: int | None,
    filepath: str | Path,
) -> None:
    """Serialize parameters, policy identity, and seed as a JSON scenario."""
    if not policy_name:
        raise ValueError("policy_name must not be empty.")
    scenario = {
        "parameters": parameters.to_dict(),
        "policy_name": policy_name,
        "seed": seed,
    }
    with Path(filepath).open("w", encoding="utf-8") as stream:
        json.dump(scenario, stream, indent=2, sort_keys=True)


def load_and_run(filepath: str | Path) -> list[SprintState]:
    """Load a saved scenario, reconstruct its policy, and run its trajectory."""
    with Path(filepath).open(encoding="utf-8") as stream:
        scenario = json.load(stream)
    policy_name = scenario["policy_name"]
    policy_type = POLICY_REGISTRY.get(policy_name)
    if policy_type is None:
        raise ValueError(f"Unknown policy: {policy_name}.")
    parameters = ModelParameters(**scenario["parameters"])
    return simulate_deterministic_sprints(parameters, policy=policy_type())
