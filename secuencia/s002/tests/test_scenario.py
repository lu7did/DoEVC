"""Regression tests for JSON scenario persistence."""

import json

from doevc_s002 import (
    DebtFirstPolicy,
    ModelParameters,
    load_and_run,
    save_scenario,
    simulate_deterministic_sprints,
)


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


def test_load_and_run_reconstructs_the_saved_policy_and_parameters(
    tmp_path: object,
) -> None:
    """Reproduce the exact deterministic trajectory through a JSON round-trip."""
    filepath = tmp_path / "scenario.json"  # type: ignore[operator]
    parameters = ModelParameters(10, 4, 5, 0, 0, 0, 0, 0, 0, 3)
    policy = DebtFirstPolicy()
    save_scenario(parameters, type(policy).__name__, 42, filepath)

    assert load_and_run(filepath) == simulate_deterministic_sprints(
        parameters, policy=policy
    )
