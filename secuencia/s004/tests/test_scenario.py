"""Tests for JSON scenario persistence."""

import json
from dataclasses import replace
from pathlib import Path

from s004 import save_scenario
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
