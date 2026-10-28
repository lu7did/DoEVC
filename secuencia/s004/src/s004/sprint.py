"""One-sprint deterministic simulation."""

from dataclasses import asdict, dataclass
from numbers import Real

from .models import ModelParameters
from .velocity import calculate_effective_velocity


def _require_non_negative(name: str, value: object) -> None:
    """Validate a non-negative real-valued sprint input."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if value < 0:
        raise ValueError(f"{name} must not be negative.")


def _require_fraction(name: str, value: object) -> None:
    """Validate a real-valued fraction in the closed unit interval."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    numeric_value = float(value)
    if numeric_value < 0 or numeric_value > 1:
        raise ValueError(f"{name} must be between zero and one.")


@dataclass(frozen=True, slots=True)
class SprintState:  # pylint: disable=too-many-instance-attributes
    """Store the input, calculated capacity, and next state of a sprint."""

    backlog: float
    technical_debt: float
    effective_velocity: float
    remediation_fraction: float
    feature_capacity: float
    remediation_capacity: float
    next_backlog: float
    next_technical_debt: float

    def __post_init__(self) -> None:
        """Validate all sprint state values."""
        for field_name in (
            "backlog",
            "technical_debt",
            "effective_velocity",
            "feature_capacity",
            "remediation_capacity",
            "next_backlog",
            "next_technical_debt",
        ):
            _require_non_negative(field_name, getattr(self, field_name))
        _require_fraction("remediation_fraction", self.remediation_fraction)

    def to_dict(self) -> dict[str, float]:
        """Return a serialization-friendly representation of this state."""
        return asdict(self)


def simulate_sprint(
    parameters: ModelParameters,
    backlog: float,
    technical_debt: float,
    remediation_fraction: float,
) -> SprintState:
    """Advance the model one sprint using a fixed remediation fraction."""
    _require_non_negative("backlog", backlog)
    _require_non_negative("technical_debt", technical_debt)
    _require_fraction("remediation_fraction", remediation_fraction)

    effective_velocity = calculate_effective_velocity(parameters, technical_debt)
    remediation_capacity = remediation_fraction * effective_velocity
    feature_capacity = (1 - remediation_fraction) * effective_velocity
    next_backlog = max(0.0, backlog - feature_capacity)
    next_technical_debt = max(
        0.0,
        technical_debt
        - remediation_capacity
        + parameters.alpha * feature_capacity
        + parameters.beta * remediation_capacity,
    )

    return SprintState(
        backlog=backlog,
        technical_debt=technical_debt,
        effective_velocity=effective_velocity,
        remediation_fraction=remediation_fraction,
        feature_capacity=feature_capacity,
        remediation_capacity=remediation_capacity,
        next_backlog=next_backlog,
        next_technical_debt=next_technical_debt,
    )
