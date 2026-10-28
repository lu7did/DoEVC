"""Tests for effective velocity calculations."""

import pytest

from s004 import ModelParameters, calculate_effective_velocity


def create_parameters() -> ModelParameters:
    """Return a representative valid parameter set."""
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
    )


def test_effective_velocity_equals_base_velocity_without_debt() -> None:
    """Zero debt leaves the base velocity unchanged."""
    parameters = create_parameters()

    assert calculate_effective_velocity(parameters, technical_debt=0.0) == 12.0


def test_effective_velocity_decreases_as_debt_increases() -> None:
    """More debt reduces effective velocity monotonically."""
    parameters = create_parameters()
    low_debt = calculate_effective_velocity(parameters, technical_debt=10.0)
    high_debt = calculate_effective_velocity(parameters, technical_debt=40.0)

    assert high_debt < low_debt


def test_effective_velocity_is_positive_for_valid_parameters() -> None:
    """Valid parameters and debt always produce a positive velocity."""
    parameters = create_parameters()

    assert calculate_effective_velocity(parameters, technical_debt=10_000.0) > 0.0


def test_effective_velocity_rejects_negative_debt() -> None:
    """Debt cannot be negative."""
    parameters = create_parameters()

    with pytest.raises(ValueError, match="technical_debt must not be negative"):
        calculate_effective_velocity(parameters, technical_debt=-0.1)
