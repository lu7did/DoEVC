"""Regression tests for JSON scenario persistence."""

import json

from doevc_s002 import ModelParameters, save_scenario


def test_save_scenario_writes_all_reproducibility_fields(tmp_path: object) -> None:
    """Write parameters, policy class name, and seed as standard JSON."""
    filepath = tmp_path / "scenario.json"  # type: ignore[operator]
    parameters = ModelParameters(10, 2, 5, 0.1, 0.2, 0.01, 0.3, 0.4, 0.5, 3)

    save_scenario(parameters, "DebtFirstPolicy", 42, filepath)

    with filepath.open(encoding="utf-8") as stream:
        scenario = json.load(stream)
    assert scenario["policy_name"] == "DebtFirstPolicy"
    assert scenario["seed"] == 42
    assert scenario["parameters"] == parameters.to_dict()
