"""Deterministic multi-sprint simulations."""

from numbers import Real

from .models import ModelParameters
from .policies import DebtFirstPolicy
from .sprint import SprintState, simulate_sprint


def simulate_deterministic_sprints(
    parameters: ModelParameters,
    remediation_fraction: Real | None = None,
    *,
    policy: DebtFirstPolicy | None = None,
) -> list[SprintState]:
    """Simulate up to K fixed-split or policy-driven sprints."""
    if policy is None:
        if isinstance(remediation_fraction, bool) or not isinstance(
            remediation_fraction, Real
        ):
            raise TypeError("remediation_fraction must be a real number.")
        if not 0 <= remediation_fraction <= 1:
            raise ValueError("remediation_fraction must be between 0 and 1.")

    backlog = parameters.B0
    debt = parameters.D0
    states: list[SprintState] = []

    for _ in range(parameters.K):
        if backlog == 0 and debt == 0:
            break

        fraction = policy.decide_u(debt) if policy is not None else remediation_fraction
        state = simulate_sprint(parameters, backlog, debt, fraction)
        states.append(state)
        backlog = state.next_backlog
        debt = state.next_debt

    return states
