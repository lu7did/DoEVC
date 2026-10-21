"""Regression tests for effective velocity in s003."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s003 import ModelParameters, calculate_effective_velocity


def _parameters(*, velocity: float = 10, gamma: float = 0.1) -> ModelParameters:
    """Create valid inputs for velocity scenarios."""
    return ModelParameters(10, 2, velocity, 0, 0, gamma, 0, 0, 0, 2)


def test_zero_debt_preserves_base_velocity() -> None:
    """Return V0 when the team carries no debt."""
    parameters = _parameters()

    assert calculate_effective_velocity(parameters, 0) == parameters.V0


def test_velocity_decreases_as_debt_increases() -> None:
    """Decrease productivity monotonically under higher debt."""
    parameters = _parameters()

    assert calculate_effective_velocity(parameters, 10) > calculate_effective_velocity(
        parameters, 20
    )


@given(
    debt=st.floats(min_value=0, max_value=1_000, allow_nan=False),
    additional_debt=st.floats(min_value=0, max_value=1_000, allow_nan=False),
)
def test_effective_velocity_is_positive_and_non_increasing(
    debt: float, additional_debt: float
) -> None:
    """Keep velocity positive as valid debt grows."""
    parameters = _parameters()

    assert calculate_effective_velocity(parameters, debt) > 0
    assert calculate_effective_velocity(
        parameters, debt + additional_debt
    ) <= calculate_effective_velocity(parameters, debt)


def test_non_positive_base_velocity_is_rejected() -> None:
    """Reject a base velocity unable to satisfy the positive-output invariant."""
    with pytest.raises(ValueError, match="V0"):
        calculate_effective_velocity(_parameters(velocity=0), 1)
