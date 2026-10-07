"""Single-sprint deterministic model transitions."""

from dataclasses import asdict, dataclass
from numbers import Real

from .models import ModelParameters
from .velocity import calculate_effective_velocity


def _validate_non_negative(name: str, value: Real) -> None:
    """Ensure a sprint quantity is a non-negative real number."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")


@dataclass(frozen=True, slots=True)
class SprintState:
    """Complete input and output state for one deterministic sprint."""

    backlog: float
    debt: float
    velocity: float
    remediation_fraction: float
    remediation_capacity: float
    feature_capacity: float
    next_backlog: float
    next_debt: float

    def to_dict(self) -> dict[str, float]:
        """Return a serializable sprint-state representation."""
        return asdict(self)


def simulate_sprint(
    parameters: ModelParameters,
    backlog: Real,
    debt: Real,
    remediation_fraction: Real,
) -> SprintState:
    """Advance backlog and debt by one sprint with a fixed remediation split."""
    _validate_non_negative("backlog", backlog)
    _validate_non_negative("debt", debt)
    if isinstance(remediation_fraction, bool) or not isinstance(
        remediation_fraction, Real
    ):
        raise TypeError("remediation_fraction must be a real number.")
    if not 0 <= remediation_fraction <= 1:
        raise ValueError("remediation_fraction must be between 0 and 1.")

    velocity = calculate_effective_velocity(parameters, debt)
    remediation_capacity = remediation_fraction * velocity
    feature_capacity = (1 - remediation_fraction) * velocity
    next_backlog = max(0.0, backlog - feature_capacity)
    next_debt = max(
        0.0,
        debt
        - remediation_capacity
        + parameters.alpha * feature_capacity
        + parameters.beta * remediation_capacity,
    )

    return SprintState(
        backlog=float(backlog),
        debt=float(debt),
        velocity=velocity,
        remediation_fraction=float(remediation_fraction),
        remediation_capacity=remediation_capacity,
        feature_capacity=feature_capacity,
        next_backlog=next_backlog,
        next_debt=next_debt,
    )
