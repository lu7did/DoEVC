"""Deterministic multi-sprint simulation."""

from numbers import Real

from .models import ModelParameters
from .policies import Policy
from .sprint import SprintState, simulate_sprint


def _require_non_negative(name: str, value: object) -> None:
    """Validate a non-negative real-valued simulation input."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if value < 0:
        raise ValueError(f"{name} must not be negative.")


def _build_policy_state(backlog: float, technical_debt: float) -> SprintState:
    """Create the current state supplied to a remediation policy."""
    return SprintState(
        backlog=backlog,
        technical_debt=technical_debt,
        effective_velocity=0.0,
        remediation_fraction=0.0,
        feature_capacity=0.0,
        remediation_capacity=0.0,
        next_backlog=backlog,
        next_technical_debt=technical_debt,
    )


def simulate_deterministic_sprints(
    parameters: ModelParameters,
    remediation_fraction: float | Policy,
    *,
    backlog: float | None = None,
    technical_debt: float | None = None,
) -> tuple[SprintState, ...]:
    """Simulate up to ``K`` sprints with a fixed fraction or decision policy."""
    current_backlog = parameters.B0 if backlog is None else backlog
    current_technical_debt = parameters.D0 if technical_debt is None else technical_debt
    _require_non_negative("backlog", current_backlog)
    _require_non_negative("technical_debt", current_technical_debt)

    trajectory: list[SprintState] = []
    for _ in range(parameters.K):
        if current_backlog == 0 and current_technical_debt == 0:
            break
        if isinstance(remediation_fraction, Policy):
            current_fraction = remediation_fraction.decide_u(
                _build_policy_state(current_backlog, current_technical_debt),
                parameters,
            )
        else:
            current_fraction = remediation_fraction

        state = simulate_sprint(
            parameters,
            backlog=current_backlog,
            technical_debt=current_technical_debt,
            remediation_fraction=current_fraction,
        )
        trajectory.append(state)
        current_backlog = state.next_backlog
        current_technical_debt = state.next_technical_debt

    return tuple(trajectory)
