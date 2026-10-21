"""Regression tests for allocation policies in s003."""

import pytest

from doevc_s003 import (
    ModelParameters,
    backlog_first_allocation,
    debt_first_allocation,
    simulate_sprints,
)


def _parameters(*, debt: float) -> ModelParameters:
    """Create a policy scenario whose debt clears in one sprint."""
    return ModelParameters(100, debt, 10, 0, 0, 0, 0, 0, 0, 2)


def test_debt_first_allocates_all_capacity_when_debt_remains() -> None:
    """Select full remediation for a positive debt state."""
    assert debt_first_allocation(10, 0.01) == 1


def test_debt_first_allocates_no_capacity_when_debt_is_cleared() -> None:
    """Select full delivery after technical debt is eliminated."""
    assert debt_first_allocation(10, 0) == 0


def test_debt_first_policy_is_selected_by_multi_sprint_simulation() -> None:
    """Recalculate policy allocation from each linked sprint state."""
    trajectory = simulate_sprints(_parameters(debt=5), debt_first_allocation)

    assert [state.allocation for state in trajectory] == [1, 0]
    assert trajectory[0].next_debt == 0
    assert trajectory[1].delivery_capacity == 10


def test_debt_first_rejects_negative_debt() -> None:
    """Reject debt values that are outside the model domain."""
    with pytest.raises(ValueError, match="debt"):
        debt_first_allocation(10, -0.1)


def test_backlog_first_allocates_no_capacity_to_remediation_with_backlog() -> None:
    """Select full delivery while functional work remains."""
    assert backlog_first_allocation(0.01, 10) == 0


def test_backlog_first_allocates_all_capacity_when_only_debt_remains() -> None:
    """Select full remediation after functional backlog is cleared."""
    assert backlog_first_allocation(0, 0.01) == 1


def test_backlog_first_policy_is_selected_by_multi_sprint_simulation() -> None:
    """Switch from delivery to remediation as the linked state changes."""
    trajectory = simulate_sprints(
        ModelParameters(5, 5, 10, 0, 0, 0, 0, 0, 0, 2),
        backlog_first_allocation,
    )

    assert [state.allocation for state in trajectory] == [0, 1]
    assert trajectory[0].next_backlog == 0
    assert trajectory[1].next_debt == 0
