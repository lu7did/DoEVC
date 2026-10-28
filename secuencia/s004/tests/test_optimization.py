"""Tests for fixed remediation grid search."""

import pytest

from s004 import (
    DebtFirstPolicy,
    ObjectiveFunction,
    OptimalLocalPolicy,
    Policy,
    grid_search_remediation,
    simulate_deterministic_sprints,
)
from tests.support import create_backlog_only_parameters, create_competing_parameters


def test_grid_search_finds_fraction_that_minimizes_objective() -> None:
    """Minimizing the final backlog selects no remediation."""
    result = grid_search_remediation(
        create_backlog_only_parameters(),
        lambda trajectory: trajectory[-1].next_backlog,
        step=0.5,
    )

    assert result.best_remediation_fraction == 0.0
    assert result.best_objective_value == 0.0
    assert len(result.evaluations) == 3


def test_grid_search_finds_fraction_that_maximizes_objective() -> None:
    """Maximizing the final backlog selects full remediation."""
    result = grid_search_remediation(
        create_backlog_only_parameters(),
        lambda trajectory: trajectory[-1].next_backlog,
        step=0.5,
        maximize=True,
    )

    assert result.best_remediation_fraction == 1.0
    assert result.best_objective_value == 10.0


def test_grid_search_includes_default_grid_endpoints() -> None:
    """The default grid evaluates every hundredth from zero through one."""
    result = grid_search_remediation(
        create_backlog_only_parameters(),
        lambda trajectory: trajectory[-1].next_backlog,
    )

    assert len(result.evaluations) == 101
    assert result.evaluations[0].remediation_fraction == 0.0
    assert result.evaluations[-1].remediation_fraction == 1.0


def test_grid_search_rejects_steps_that_do_not_divide_unit_interval() -> None:
    """The grid only accepts exact divisions of the unit interval."""
    with pytest.raises(ValueError, match="step must divide the unit interval"):
        grid_search_remediation(
            create_backlog_only_parameters(),
            lambda trajectory: trajectory[-1].next_backlog,
            step=0.3,
        )


def test_economic_objective_weights_produce_distinct_optima() -> None:
    """Feature- and debt-focused objectives select different allocations."""
    parameters = create_competing_parameters()
    feature_focused = grid_search_remediation(
        parameters,
        ObjectiveFunction(
            delivered_functionality_weight=2.0,
            remaining_debt_penalty=1.0,
        ),
        step=1.0,
        maximize=True,
    )
    debt_focused = grid_search_remediation(
        parameters,
        ObjectiveFunction(
            delivered_functionality_weight=1.0,
            remaining_debt_penalty=2.0,
        ),
        step=1.0,
        maximize=True,
    )

    assert feature_focused.best_remediation_fraction == 0.0
    assert debt_focused.best_remediation_fraction == 1.0


def test_optimal_local_policy_outperforms_debt_first_for_feature_value() -> None:
    """The locally optimized allocation improves the selected objective."""
    parameters = create_competing_parameters()
    objective = ObjectiveFunction(
        delivered_functionality_weight=2.0,
        remaining_debt_penalty=1.0,
    )
    policy = OptimalLocalPolicy(objective, step=1.0)
    optimal_trajectory = simulate_deterministic_sprints(parameters, policy)
    debt_first_trajectory = simulate_deterministic_sprints(
        parameters,
        DebtFirstPolicy(),
    )

    assert isinstance(policy, Policy)
    assert optimal_trajectory[0].remediation_fraction == 0.0
    assert objective(optimal_trajectory) > objective(debt_first_trajectory)
