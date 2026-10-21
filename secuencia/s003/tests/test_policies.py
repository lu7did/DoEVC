"""Regression tests for interchangeable policies in s003."""

import pytest

from doevc_s003 import (
    BacklogFirstPolicy,
    DebtFirstPolicy,
    ModelParameters,
    Policy,
    ProportionalPolicy,
    SprintState,
    simulate_sprints,
)


def _parameters(*, backlog: float = 100, debt: float = 5) -> ModelParameters:
    """Create a policy scenario whose state changes within two sprints."""
    return ModelParameters(backlog, debt, 10, 0, 0, 0, 0, 0, 0, 2)


def _state(backlog: float, debt: float) -> SprintState:
    """Create the current state supplied to a policy decision."""
    return SprintState.current(backlog, debt)


def test_debt_first_selects_remediation_until_debt_is_cleared() -> None:
    """Select full remediation only while debt remains."""
    policy = DebtFirstPolicy()

    assert policy.decide_u(_state(10, 0.01), _parameters()) == 1
    assert policy.decide_u(_state(10, 0), _parameters()) == 0


def test_backlog_first_selects_delivery_until_backlog_is_cleared() -> None:
    """Select delivery before remediation when functional work remains."""
    policy = BacklogFirstPolicy()

    assert policy.decide_u(_state(0.01, 10), _parameters()) == 0
    assert policy.decide_u(_state(0, 0.01), _parameters()) == 1


def test_proportional_policy_handles_general_and_boundary_states() -> None:
    """Return the relative debt fraction without dividing by zero."""
    policy = ProportionalPolicy()

    assert policy.decide_u(_state(3, 1), _parameters()) == 0.25
    assert policy.decide_u(_state(10, 0), _parameters()) == 0
    assert policy.decide_u(_state(0, 10), _parameters()) == 1
    assert policy.decide_u(_state(0, 0), _parameters()) == 0


@pytest.mark.parametrize(
    "policy",
    [DebtFirstPolicy(), BacklogFirstPolicy(), ProportionalPolicy()],
)
def test_each_policy_implements_the_common_protocol_and_runs_in_simulation(
    policy: Policy,
) -> None:
    """Allow every policy to be exchanged by the deterministic engine."""
    trajectory = simulate_sprints(_parameters(), policy)

    assert isinstance(policy, Policy)
    assert len(trajectory) == 2
    assert all(0 <= state.allocation <= 1 for state in trajectory)


def test_debt_first_policy_recomputes_allocation_for_linked_sprints() -> None:
    """Switch to delivery after the previous sprint clears the debt."""
    trajectory = simulate_sprints(_parameters(), DebtFirstPolicy())

    assert [state.allocation for state in trajectory] == [1, 0]
