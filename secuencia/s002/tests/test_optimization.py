"""Regression tests for remediation grid search."""

from doevc_s002 import ModelParameters, ObjectiveFunction, grid_search_remediation


def _parameters() -> ModelParameters:
    """Create a model where debt-only work minimizes final debt."""
    return ModelParameters(10, 10, 10, 0, 0, 0, 0, 0, 0, 1)


def test_grid_search_finds_the_minimizing_fraction() -> None:
    """Select full remediation when minimizing final debt."""
    result = grid_search_remediation(
        _parameters(), lambda states: states[-1].next_debt, step=0.5
    )

    assert result.remediation_fraction == 1.0
    assert set(result.trajectories) == {0.0, 0.5, 1.0}


def test_grid_search_can_maximize_a_custom_objective() -> None:
    """Select feature work when maximizing final delivered capacity."""
    result = grid_search_remediation(
        _parameters(),
        lambda states: states[-1].feature_capacity,
        step=0.5,
        maximize=True,
    )

    assert result.remediation_fraction == 0.0


def test_economic_weights_change_the_optimal_fraction() -> None:
    """Prioritize delivery or debt reduction according to configured weights."""
    delivery_first = grid_search_remediation(
        _parameters(), ObjectiveFunction(1, 0), step=0.5, maximize=True
    )
    debt_first = grid_search_remediation(
        _parameters(), ObjectiveFunction(0, 1), step=0.5, maximize=True
    )

    assert delivery_first.remediation_fraction == 0.0
    assert debt_first.remediation_fraction == 1.0
