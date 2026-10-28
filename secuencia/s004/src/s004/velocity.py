"""Effective velocity calculations."""

from numbers import Real

from .models import ModelParameters


def calculate_effective_velocity(
    parameters: ModelParameters,
    technical_debt: float,
) -> float:
    """Calculate velocity after the productivity loss caused by debt."""
    if isinstance(technical_debt, bool) or not isinstance(technical_debt, Real):
        raise TypeError("technical_debt must be a real number.")
    if technical_debt < 0:
        raise ValueError("technical_debt must not be negative.")

    return parameters.V0 / (1 + parameters.gamma * technical_debt)
