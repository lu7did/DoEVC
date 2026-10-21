"""Effective productivity calculations."""

from numbers import Real

from .models import ModelParameters


def calculate_effective_velocity(parameters: ModelParameters, debt: object) -> float:
    """Calculate velocity after the productivity impact of technical debt."""
    if isinstance(debt, bool) or not isinstance(debt, Real):
        raise TypeError("debt must be a real number.")
    if debt < 0:
        raise ValueError("debt must not be negative.")
    if parameters.V0 <= 0:
        raise ValueError("parameters.V0 must be positive.")

    debt_value = float(debt)
    return parameters.V0 / (1 + parameters.gamma * debt_value)
