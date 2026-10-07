"""Effective velocity calculations."""

from numbers import Real

from .models import ModelParameters


def calculate_effective_velocity(parameters: ModelParameters, debt: Real) -> float:
    """Calculate the productive velocity remaining after technical debt."""
    if isinstance(debt, bool) or not isinstance(debt, Real):
        raise TypeError("debt must be a real number.")
    if debt < 0:
        raise ValueError("debt must be non-negative.")
    if parameters.V0 <= 0:
        raise ValueError("parameters.V0 must be positive.")

    return parameters.V0 / (1 + parameters.gamma * debt)
