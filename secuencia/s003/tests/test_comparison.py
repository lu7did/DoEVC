"""Regression tests for policy comparisons in s003."""

from doevc_s003 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    EconomicObjective,
    ModelParameters,
    Policy,
    ProportionalPolicy,
    compare_policies,
)


def _parameters() -> ModelParameters:
    """Create a scenario whose candidate policies make distinct choices."""
    return ModelParameters(10, 10, 10, 0, 0, 0, 0, 0, 0, 1)


def _policies() -> dict[str, Policy]:
    """Name the baseline policies compared on a shared scenario."""
    return {
        "backlog": BacklogFirstPolicy(),
        "debt": DebtFirstPolicy(),
        "proportional": ProportionalPolicy(),
    }


def test_comparison_includes_every_policy_with_distinct_deterministic_metrics() -> None:
    """Return one C3 metrics row for every named policy on the same inputs."""
    table = compare_policies(
        _parameters(),
        _policies(),
        EconomicObjective(delivery_weight=1, debt_weight=2),
    )

    assert [row.name for row in table.rows] == ["backlog", "debt", "proportional"]
    final_states = {
        (row.result.metrics.final_backlog.mean, row.result.metrics.final_debt.mean)
        for row in table.rows
    }
    assert len(final_states) == 3


def test_comparison_uses_equivalent_samples_for_each_monte_carlo_policy() -> None:
    """Reuse the configured seed so each policy faces matching sampled parameters."""
    table = compare_policies(
        _parameters(),
        {"backlog": BacklogFirstPolicy(), "debt": DebtFirstPolicy()},
        EconomicObjective(),
        n_runs=2,
        seed=9,
    )

    assert all(len(row.result.runs) == 2 for row in table.rows)
    assert [run.parameters for run in table.rows[0].result.runs] == [
        run.parameters for run in table.rows[1].result.runs
    ]
