"""Deterministic multi-sprint simulation helpers for DoEVC s001."""

from .models import ModelParameters, ensure_non_negative
from .sprint import SprintState, simulate_sprint


def simulate_deterministic_sprints(
    parameters: ModelParameters,
    remediation_fraction: float,
    *,
    backlog: float | None = None,
    technical_debt: float | None = None,
) -> tuple[SprintState, ...]:
    """Simulate up to ``K`` deterministic sprints using a fixed remediation split."""
    current_backlog = parameters.B0 if backlog is None else backlog
    current_technical_debt = parameters.D0 if technical_debt is None else technical_debt

    ensure_non_negative("backlog", current_backlog)
    ensure_non_negative("technical_debt", current_technical_debt)

    trajectory: list[SprintState] = []
    for _ in range(parameters.K):
        if current_backlog == 0 and current_technical_debt == 0:
            break

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
