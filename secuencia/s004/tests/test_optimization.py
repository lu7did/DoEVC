"""Tests for fixed remediation grid search."""

import pytest

from s004 import ModelParameters, ObjectiveFunction, grid_search_remediation


def create_backlog_only_parameters() -> ModelParameters:
    """Return a one-sprint model with known fixed-fraction outcomes."""
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
    )


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
    parameters = ModelParameters(
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
    )
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
