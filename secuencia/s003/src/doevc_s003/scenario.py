"""Portable JSON scenario serialization."""

import json
from pathlib import Path

from .models import ModelParameters


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
