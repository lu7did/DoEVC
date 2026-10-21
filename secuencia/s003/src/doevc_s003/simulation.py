"""Deterministic multi-sprint simulations."""

from .models import ModelParameters
from .policies import Policy
from .sprint import SprintState, simulate_sprint


def simulate_sprints(
    parameters: ModelParameters, allocation: float | Policy
) -> list[SprintState]:
    """Run up to ``K`` sprints with a fixed allocation or a ``Policy``."""
    backlog = parameters.B0
    debt = parameters.D0
    trajectory: list[SprintState] = []

    for _ in range(parameters.K):
        if backlog == 0 and debt == 0:
            break
        policy_state = SprintState.current(backlog, debt)
        current_allocation = (
            allocation.decide_u(policy_state, parameters)
            if isinstance(allocation, Policy)
            else allocation
        )
        state = simulate_sprint(parameters, backlog, debt, current_allocation)
        trajectory.append(state)
        backlog = state.next_backlog
        debt = state.next_debt

    return trajectory
