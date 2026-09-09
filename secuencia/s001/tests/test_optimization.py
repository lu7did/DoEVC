"""Tests for fixed remediation grid search."""

import pytest

from doevc_s001 import (
    DebtFirstPolicy,
    ModelParameters,
    ObjectiveFunction,
    OptimalLocalPolicy,
    Policy,
    grid_search_remediation,
    simulate_deterministic_sprints,
)


def test_grid_search_finds_the_fraction_that_minimizes_an_objective() -> None:
    """Select zero remediation when minimizing the final functional backlog."""
    result = grid_search_remediation(
        _parameters_with_only_backlog(),
        lambda trajectory: trajectory[-1].next_backlog,
        step=0.5,
    )

    assert result.best_remediation_fraction == 0.0
    assert result.best_objective_value == 0.0
    assert len(result.evaluations) == 3


def test_grid_search_finds_the_fraction_that_maximizes_an_objective() -> None:
    """Select full remediation when maximizing the final functional backlog."""
    result = grid_search_remediation(
        _parameters_with_only_backlog(),
        lambda trajectory: trajectory[-1].next_backlog,
        step=0.5,
        maximize=True,
    )

    assert result.best_remediation_fraction == 1.0
    assert result.best_objective_value == 10.0


def test_grid_search_includes_each_endpoint_with_the_default_step() -> None:
    """Evaluate every hundredth from zero through one by default."""
    result = grid_search_remediation(
        _parameters_with_only_backlog(),
        lambda trajectory: trajectory[-1].next_backlog,
    )

    assert len(result.evaluations) == 101
    assert result.evaluations[0].remediation_fraction == 0.0
    assert result.evaluations[-1].remediation_fraction == 1.0


def test_grid_search_rejects_steps_that_do_not_divide_the_unit_interval() -> None:
    """Reject a step that cannot produce a uniform inclusive grid."""
    with pytest.raises(ValueError, match="step must divide the unit interval"):
        grid_search_remediation(
            _parameters_with_only_backlog(),
            lambda trajectory: trajectory[-1].next_backlog,
            step=0.3,
        )


def test_economic_objective_weights_produce_distinct_optima() -> None:
    """Select different fractions when feature and debt weights change."""
    parameters = _parameters_with_backlog_and_debt()
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
    """Choose local feature delivery when it has greater economic value."""
    parameters = _parameters_with_backlog_and_debt()
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


def _parameters_with_only_backlog() -> ModelParameters:
    """Return a one-sprint model with a known fixed-fraction outcome."""
    return ModelParameters(
        B0=10.0,
        D0=0.0,
        V0=10.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.0,
        lambda_=0.0,
        rho=0.0,
        K=1,
        s=1.0,
    )


def _parameters_with_backlog_and_debt() -> ModelParameters:
    """Return a one-sprint model where delivery and debt compete."""
    return ModelParameters(
        B0=10.0,
        D0=10.0,
        V0=10.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.0,
        lambda_=0.0,
        rho=0.0,
        K=1,
        s=1.0,
    )
