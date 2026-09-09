"""Tests for JSON scenario persistence."""

import json

from doevc_s001 import ModelParameters, save_scenario


def test_save_scenario_writes_all_reproducibility_fields(tmp_path) -> None:
    """Serialize parameters, policy name, and seed as standard JSON."""
    params = ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=12.0,
        alpha=0.3,
        beta=0.1,
        gamma=0.05,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=16,
        s=1.1,
    )
    filepath = tmp_path / "scenario.json"

    save_scenario(params, "ProportionalPolicy", 1234, filepath)

    with filepath.open(encoding="utf-8") as json_file:
        scenario = json.load(json_file)

    assert scenario == {
        "parameters": params.to_dict(),
        "policy_name": "ProportionalPolicy",
        "seed": 1234,
    }
