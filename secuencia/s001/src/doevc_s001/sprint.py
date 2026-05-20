"""One-sprint deterministic simulation helpers for the DoEVC s001 sequence."""

from dataclasses import dataclass

from .models import ModelParameters, _ensure_non_negative
from .velocity import calculate_effective_velocity


def _ensure_fraction(name: str, value: float) -> None:
    """Ensure that a fraction lies inside the closed unit interval."""
    if value < 0 or value > 1:
        raise ValueError(f"{name} must be between 0 and 1.")


@dataclass(slots=True, frozen=True)
class SprintState:
    """Store the current and next deterministic state of one sprint."""

    backlog: float
    technical_debt: float
    effective_velocity: float
    remediation_fraction: float
    feature_capacity: float
    remediation_capacity: float
    next_backlog: float
    next_technical_debt: float

    def __post_init__(self) -> None:
        """Validate the simulated sprint state."""
        _ensure_non_negative("backlog", self.backlog)
        _ensure_non_negative("technical_debt", self.technical_debt)
        _ensure_non_negative("effective_velocity", self.effective_velocity)
        _ensure_fraction("remediation_fraction", self.remediation_fraction)
        _ensure_non_negative("feature_capacity", self.feature_capacity)
        _ensure_non_negative("remediation_capacity", self.remediation_capacity)
        _ensure_non_negative("next_backlog", self.next_backlog)
        _ensure_non_negative("next_technical_debt", self.next_technical_debt)

    def to_dict(self) -> dict[str, float]:
        """Serialize the sprint state to a dictionary."""
        return {
            "backlog": self.backlog,
            "technical_debt": self.technical_debt,
            "effective_velocity": self.effective_velocity,
            "remediation_fraction": self.remediation_fraction,
            "feature_capacity": self.feature_capacity,
            "remediation_capacity": self.remediation_capacity,
            "next_backlog": self.next_backlog,
            "next_technical_debt": self.next_technical_debt,
        }


def simulate_sprint(
    parameters: ModelParameters,
    backlog: float,
    technical_debt: float,
    remediation_fraction: float,
) -> SprintState:
    """Advance the deterministic model by one sprint with a fixed remediation split."""
    _ensure_non_negative("backlog", backlog)
    _ensure_non_negative("technical_debt", technical_debt)
    _ensure_fraction("remediation_fraction", remediation_fraction)

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
