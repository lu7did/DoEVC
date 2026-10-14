"""Regression tests for policy comparison."""

from doevc_s002 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    ModelParameters,
    ObjectiveFunction,
    compare_policies,
)


def test_comparison_includes_each_policy_with_distinct_results() -> None:
    """Evaluate all supplied policies on the same deterministic scenario."""
    parameters = ModelParameters(10, 10, 10, 0, 0, 0, 0, 0, 0, 1)
    results = compare_policies(
        parameters, [DebtFirstPolicy(), BacklogFirstPolicy()], ObjectiveFunction(1, 0)
    )

    assert set(results) == {"DebtFirstPolicy", "BacklogFirstPolicy"}
    assert (
        results["DebtFirstPolicy"].objective_value
        != results["BacklogFirstPolicy"].objective_value
    )
