"""Deterministic multi-sprint simulations."""

from .models import ModelParameters
from .sprint import SprintState, simulate_sprint


def simulate_sprints(
    parameters: ModelParameters, allocation: object
) -> list[SprintState]:
    """Run up to ``K`` connected sprints with a fixed remediation allocation."""
    backlog = parameters.B0
    debt = parameters.D0
    trajectory: list[SprintState] = []

    for _ in range(parameters.K):
        if backlog == 0 and debt == 0:
            break
        state = simulate_sprint(parameters, backlog, debt, allocation)
        trajectory.append(state)
        backlog = state.next_backlog
        debt = state.next_debt

    return trajectory
