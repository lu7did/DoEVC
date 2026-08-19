"""Tests for effective velocity calculations in DoEVC s001."""

import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s001 import ModelParameters, calculate_effective_velocity


def sample_parameters() -> ModelParameters:
    """Return a representative parameter set for velocity tests."""
    return ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=12.0,
        alpha=0.3,
        beta=0.1,
        gamma=0.05,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=16,
        s=1.0,
    )


def test_effective_velocity_matches_base_velocity_without_debt() -> None:
    """Return V0 when the current technical debt is zero."""
    parameters = sample_parameters()

    assert calculate_effective_velocity(parameters, technical_debt=0.0) == parameters.V0


def test_effective_velocity_decreases_when_debt_grows() -> None:
    """Decrease the effective velocity as technical debt increases."""
    parameters = sample_parameters()

    low_debt_velocity = calculate_effective_velocity(parameters, technical_debt=10.0)
    high_debt_velocity = calculate_effective_velocity(parameters, technical_debt=40.0)

    assert high_debt_velocity < low_debt_velocity


def test_effective_velocity_is_always_positive_for_valid_parameters() -> None:
    """Keep the effective velocity strictly positive for valid inputs."""
    parameters = sample_parameters()

    result = calculate_effective_velocity(parameters, technical_debt=10_000.0)

    assert result > 0.0


def test_effective_velocity_rejects_negative_technical_debt() -> None:
    """Reject negative technical debt values."""
    with pytest.raises(ValueError, match="technical_debt must be non-negative"):
        calculate_effective_velocity(sample_parameters(), technical_debt=-0.1)


@given(
    v0=st.floats(min_value=0.1, max_value=1_000, allow_infinity=False, allow_nan=False),
    gamma=st.floats(min_value=0, max_value=1, allow_infinity=False, allow_nan=False),
    technical_debt=st.floats(
        min_value=0, max_value=1_000, allow_infinity=False, allow_nan=False
    ),
)
def test_effective_velocity_matches_formula(
    v0: float,
    gamma: float,
    technical_debt: float,
) -> None:
    """Match the expected analytical formula for effective velocity."""
    parameters = ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=v0,
        alpha=0.3,
        beta=0.1,
        gamma=gamma,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=16,
        s=1.0,
    )

    result = calculate_effective_velocity(parameters, technical_debt=technical_debt)
    expected = v0 / (1 + gamma * technical_debt)

    assert math.isclose(result, expected)
