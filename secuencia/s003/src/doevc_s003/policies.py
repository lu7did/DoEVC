"""Allocation policies for deterministic simulations."""

from numbers import Real


def debt_first_allocation(debt: object) -> float:
    """Allocate all capacity to remediation while technical debt remains."""
    if isinstance(debt, bool) or not isinstance(debt, Real):
        raise TypeError("debt must be a real number.")
    debt_value = float(debt)
    if debt_value < 0:
        raise ValueError("debt must not be negative.")
    return 1.0 if debt_value > 0 else 0.0
