"""Scenario persistence helpers."""

import json
from pathlib import Path

from .models import ModelParameters


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
