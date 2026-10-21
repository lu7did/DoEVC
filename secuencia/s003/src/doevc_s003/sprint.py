"""Single-sprint state transitions."""

from dataclasses import dataclass
from numbers import Real

from .models import ModelParameters
from .velocity import calculate_effective_velocity


def _require_non_negative_real(name: str, value: object) -> float:
    """Return a valid non-negative real value."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if value < 0:
        raise ValueError(f"{name} must not be negative.")
    return float(value)


def _require_allocation(value: object) -> float:
    """Return a valid remediation allocation between zero and one."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError("allocation must be a real number.")
    allocation = float(value)
    if not 0 <= allocation <= 1:
        raise ValueError("allocation must be between 0 and 1.")
    return allocation


@dataclass(frozen=True, slots=True)
class SprintState:  # pylint: disable=too-many-instance-attributes
    """Inputs, capacity allocation, and resulting state for one sprint."""

    backlog: float
    debt: float
    allocation: float
    velocity: float
    remediation_capacity: float
    delivery_capacity: float
    next_backlog: float
    next_debt: float


def simulate_sprint(
    parameters: ModelParameters, backlog: object, debt: object, allocation: object
) -> SprintState:
    """Calculate the next backlog and debt state for a fixed allocation."""
    current_backlog = _require_non_negative_real("backlog", backlog)
    current_debt = _require_non_negative_real("debt", debt)
    remediation_allocation = _require_allocation(allocation)
    velocity = calculate_effective_velocity(parameters, current_debt)
    remediation_capacity = remediation_allocation * velocity
    delivery_capacity = (1 - remediation_allocation) * velocity
    next_backlog = max(0.0, current_backlog - delivery_capacity)
    next_debt = max(
        0.0,
        current_debt
        - remediation_capacity
        + parameters.alpha * delivery_capacity
        + parameters.beta * remediation_capacity,
    )
    return SprintState(
        backlog=current_backlog,
        debt=current_debt,
        allocation=remediation_allocation,
        velocity=velocity,
        remediation_capacity=remediation_capacity,
        delivery_capacity=delivery_capacity,
        next_backlog=next_backlog,
        next_debt=next_debt,
    )
