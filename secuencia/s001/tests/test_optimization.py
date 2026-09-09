"""Tests for fixed remediation grid search."""

import pytest

from doevc_s001 import ModelParameters, grid_search_remediation


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
