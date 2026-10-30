"""Tests for JSON scenario persistence."""

import json
from dataclasses import replace
from pathlib import Path

from s004 import (
    DebtFirstPolicy,
    load_and_run,
    save_scenario,
    simulate_deterministic_sprints,
)
from tests.support import create_parameters


def test_save_scenario_writes_all_reproducibility_fields(tmp_path: Path) -> None:
    """Serialize parameters, policy name, and seed as standard JSON."""
    params = replace(create_parameters(), s=1.1)
    filepath = tmp_path / "scenario.json"

    save_scenario(params, "ProportionalPolicy", 1234, filepath)

    with filepath.open(encoding="utf-8") as json_file:
        scenario = json.load(json_file)

    assert scenario == {
        "parameters": params.to_dict(),
        "policy_name": "ProportionalPolicy",
        "seed": 1234,
    }


def test_save_and_load_scenario_reproduces_trajectory(tmp_path: Path) -> None:
    """A saved policy scenario round-trips to the same sprint states."""
    params = replace(create_parameters(), B0=8.0, D0=4.0, V0=4.0, K=3)
    filepath = tmp_path / "scenario.json"
    original_trajectory = simulate_deterministic_sprints(params, DebtFirstPolicy())

    save_scenario(params, "DebtFirstPolicy", 1234, filepath)

    assert load_and_run(filepath) == original_trajectory
