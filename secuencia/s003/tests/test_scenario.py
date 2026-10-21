"""Regression tests for JSON scenario serialization in s003."""

import json
from pathlib import Path

import pytest

from doevc_s003 import (
    DebtFirstPolicy,
    ModelParameters,
    load_and_run,
    save_scenario,
    simulate_sprints,
)


def test_scenario_save_writes_all_reproducibility_fields(tmp_path: Path) -> None:
    """Create a standard JSON document with every parameter and scenario input."""
    path = tmp_path / "scenario.json"
    parameters = ModelParameters(10, 2, 5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 7)

    save_scenario(parameters, "DebtFirstPolicy", 42, path)

    with path.open(encoding="utf-8") as input_file:
        scenario = json.load(input_file)
    assert scenario["policy_name"] == "DebtFirstPolicy"
    assert scenario["seed"] == 42
    assert scenario["parameters"] == parameters.to_dict()


def test_scenario_round_trip_reproduces_the_original_trajectory(tmp_path: Path) -> None:
    """Rebuild the registered policy and parameters from the saved JSON file."""
    path = tmp_path / "scenario.json"
    parameters = ModelParameters(10, 5, 5, 0, 0, 0, 0, 0, 0, 3)
    original_trajectory = simulate_sprints(parameters, DebtFirstPolicy())

    save_scenario(parameters, "DebtFirstPolicy", 42, path)

    assert load_and_run(path) == original_trajectory


def test_scenario_load_rejects_unregistered_policy_names(tmp_path: Path) -> None:
    """Reject names not present in the internal reconstruction registry."""
    path = tmp_path / "scenario.json"
    save_scenario(ModelParameters(1, 1, 1, 0, 0, 0, 0, 0, 0, 1), "Unknown", 1, path)

    with pytest.raises(ValueError, match="unsupported"):
        load_and_run(path)
