"""Velocity calculation helpers for the DoEVC s001 sequence."""

from .models import ModelParameters


def calculate_effective_velocity(
    parameters: ModelParameters,
    technical_debt: float,
) -> float:
    """Calculate sprint effective velocity degraded by technical debt."""
    if technical_debt < 0:
        raise ValueError("technical_debt must be non-negative.")

    return parameters.V0 / (1 + parameters.gamma * technical_debt)
