"""Persistence of reproducible simulation scenarios."""

import json
from pathlib import Path

from .models import ModelParameters


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
