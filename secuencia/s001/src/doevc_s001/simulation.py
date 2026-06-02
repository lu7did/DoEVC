"""Deterministic multi-sprint simulation helpers for DoEVC s001."""

from __future__ import annotations

from .models import ModelParameters, ensure_non_negative
from .policies import Policy
from .sprint import SprintState, simulate_sprint
from .velocity import calculate_effective_velocity


def _build_policy_state(
    parameters: ModelParameters,
    backlog: float,
    technical_debt: float,
) -> SprintState:
    """Create the current sprint snapshot consumed by policy objects."""
    effective_velocity = calculate_effective_velocity(parameters, technical_debt)
    return SprintState(
        backlog=backlog,
        technical_debt=technical_debt,
        effective_velocity=effective_velocity,
        remediation_fraction=0.0,
        feature_capacity=0.0,
        remediation_capacity=0.0,
        next_backlog=backlog,
        next_technical_debt=technical_debt,
    )


def simulate_deterministic_sprints(
    parameters: ModelParameters,
    policy: Policy,
    *,
    backlog: float | None = None,
    technical_debt: float | None = None,
) -> tuple[SprintState, ...]:
    """Simulate up to ``K`` sprints using any policy implementing ``Policy``."""
    current_backlog = parameters.B0 if backlog is None else backlog
    current_technical_debt = parameters.D0 if technical_debt is None else technical_debt

    ensure_non_negative("backlog", current_backlog)
    ensure_non_negative("technical_debt", current_technical_debt)

    trajectory: list[SprintState] = []
    for _ in range(parameters.K):
        if current_backlog == 0 and current_technical_debt == 0:
            break

        policy_state = _build_policy_state(
            parameters,
            backlog=current_backlog,
            technical_debt=current_technical_debt,
        )
        remediation_fraction = policy.decide_u(policy_state, parameters)
        sprint_state = simulate_sprint(
            parameters,
            backlog=current_backlog,
            technical_debt=current_technical_debt,
            remediation_fraction=remediation_fraction,
        )
        trajectory.append(sprint_state)
        current_backlog = sprint_state.next_backlog
        current_technical_debt = sprint_state.next_technical_debt

    return tuple(trajectory)
