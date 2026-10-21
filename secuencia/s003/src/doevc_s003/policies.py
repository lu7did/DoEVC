"""Allocation policies for deterministic simulations."""

from numbers import Real


def _require_non_negative(name: str, value: object) -> float:
    """Return a valid non-negative real value."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    numeric_value = float(value)
    if numeric_value < 0:
        raise ValueError(f"{name} must not be negative.")
    return numeric_value


def debt_first_allocation(backlog: object, debt: object) -> float:
    """Allocate all capacity to remediation while technical debt remains."""
    _require_non_negative("backlog", backlog)
    debt_value = _require_non_negative("debt", debt)
    return 1.0 if debt_value > 0 else 0.0


def backlog_first_allocation(backlog: object, debt: object) -> float:
    """Allocate capacity to delivery until functional backlog is cleared."""
    backlog_value = _require_non_negative("backlog", backlog)
    debt_value = _require_non_negative("debt", debt)
    if backlog_value > 0:
        return 0.0
    return 1.0 if debt_value > 0 else 0.0


def proportional_allocation(backlog: object, debt: object) -> float:
    """Allocate remediation capacity according to the relative debt level."""
    backlog_value = _require_non_negative("backlog", backlog)
    debt_value = _require_non_negative("debt", debt)
    total_work = backlog_value + debt_value
    return debt_value / total_work if total_work > 0 else 0.0
