"""Tests for JSON scenario persistence."""

import json

from doevc_s001 import (
    DebtFirstPolicy,
    ModelParameters,
    load_and_run,
    save_scenario,
    simulate_deterministic_sprints,
)


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


def test_save_and_load_scenario_reproduces_the_same_trajectory(tmp_path) -> None:
    """Round-trip a scenario and retain every generated sprint state."""
    params = ModelParameters(
        B0=8.0,
        D0=4.0,
        V0=4.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=3,
        s=1.0,
    )
    filepath = tmp_path / "scenario.json"
    original_trajectory = simulate_deterministic_sprints(params, DebtFirstPolicy())

    save_scenario(params, "DebtFirstPolicy", 1234, filepath)

    assert load_and_run(filepath) == original_trajectory
