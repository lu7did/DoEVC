"""Regression tests for effective velocity."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s002 import ModelParameters, calculate_effective_velocity


def _parameters(*, V0: float = 10.0, gamma: float = 0.2) -> ModelParameters:
    """Create a valid parameter set for velocity tests."""
    return ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=V0,
        alpha=0.5,
        beta=0.2,
        gamma=gamma,
        theta=0.3,
        lambda_=0.8,
        rho=0.4,
        K=12,
    )


def test_zero_debt_returns_base_velocity() -> None:
    """Return V0 when no technical debt is present."""
    parameters = _parameters()

    assert calculate_effective_velocity(parameters, 0) == parameters.V0


def test_velocity_decreases_when_debt_increases() -> None:
    """Decrease velocity monotonically as debt grows."""
    parameters = _parameters()

    assert calculate_effective_velocity(parameters, 10) > calculate_effective_velocity(
        parameters, 20
    )


@given(
    base_velocity=st.floats(
        min_value=0.001,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
    ),
    gamma=st.floats(
        min_value=0,
        max_value=1_000,
        allow_nan=False,
        allow_infinity=False,
    ),
    lower_debt=st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
    ),
    extra_debt=st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_effective_velocity_is_positive_and_non_increasing(
    base_velocity: float, gamma: float, lower_debt: float, extra_debt: float
) -> None:
    """Keep velocity positive and non-increasing for valid generated inputs."""
    parameters = _parameters(V0=base_velocity, gamma=gamma)
    lower_velocity = calculate_effective_velocity(parameters, lower_debt)
    higher_velocity = calculate_effective_velocity(parameters, lower_debt + extra_debt)

    assert lower_velocity > 0
    assert higher_velocity > 0
    assert higher_velocity <= lower_velocity


@pytest.mark.parametrize("debt", [-1, -0.1])
def test_negative_debt_is_rejected(debt: float) -> None:
    """Reject debt values outside the model domain."""
    with pytest.raises(ValueError, match="debt"):
        calculate_effective_velocity(_parameters(), debt)


def test_zero_base_velocity_is_rejected() -> None:
    """Reject a base velocity that cannot produce a positive result."""
    with pytest.raises(ValueError, match="V0"):
        calculate_effective_velocity(_parameters(V0=0), 10)
