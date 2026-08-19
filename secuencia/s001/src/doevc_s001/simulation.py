"""Deterministic multi-sprint simulation helpers for DoEVC s001."""

from .models import ModelParameters, ensure_non_negative
from .policies import Policy
from .sprint import SprintState, simulate_sprint


def _build_policy_state(
    backlog: float,
    technical_debt: float,
) -> SprintState:
    """Create the current sprint snapshot consumed by policy objects."""
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
    """Simulate up to ``K`` deterministic sprints with a fixed split or policy."""
    current_backlog = parameters.B0 if backlog is None else backlog
    current_technical_debt = parameters.D0 if technical_debt is None else technical_debt

    ensure_non_negative("backlog", current_backlog)
    ensure_non_negative("technical_debt", current_technical_debt)

    trajectory: list[SprintState] = []
    for _ in range(parameters.K):
        if current_backlog == 0 and current_technical_debt == 0:
            break

        if isinstance(remediation_fraction, Policy):
            current_fraction = remediation_fraction.decide_u(
                _build_policy_state(
                    backlog=current_backlog,
                    technical_debt=current_technical_debt,
                ),
                parameters,
            )
        else:
            current_fraction = remediation_fraction

        sprint_state = simulate_sprint(
            parameters,
            backlog=current_backlog,
            technical_debt=current_technical_debt,
            remediation_fraction=current_fraction,
        )
        trajectory.append(sprint_state)
        current_backlog = sprint_state.next_backlog
        current_technical_debt = sprint_state.next_technical_debt

    return tuple(trajectory)
