"""Regression tests for JSON scenario serialization in s003."""

import json
from pathlib import Path

from doevc_s003 import ModelParameters, save_scenario


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
