"""Regression tests for individual sprints in s003."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from doevc_s003 import ModelParameters, simulate_sprint


def _parameters(*, alpha: float = 0.1, beta: float = 0.2) -> ModelParameters:
    """Create valid, readable inputs for sprint scenarios."""
    return ModelParameters(20, 5, 10, alpha, beta, 0.1, 0, 0, 0, 2)


def test_sprint_returns_known_transition_values() -> None:
    """Expose all capacities and resulting states for known parameters."""
    state = simulate_sprint(_parameters(), backlog=20, debt=5, allocation=0.4)

    assert state.backlog == 20
    assert state.debt == 5
    assert state.allocation == 0.4
    assert state.velocity == pytest.approx(10 / 1.5)
    assert state.remediation_capacity == pytest.approx(8 / 3)
    assert state.delivery_capacity == pytest.approx(4)
    assert state.next_backlog == pytest.approx(16)
    assert state.next_debt == pytest.approx(3.2666666666666666)


@pytest.mark.parametrize("allocation", [-0.01, 1.01])
def test_out_of_range_allocation_is_rejected(allocation: float) -> None:
    """Reject fixed allocations outside the supported interval."""
    with pytest.raises(ValueError, match="allocation"):
        simulate_sprint(_parameters(), 10, 2, allocation)


def test_sprint_clamps_backlog_and_debt_at_zero() -> None:
    """Keep the next state non-negative when capacity exceeds the inputs."""
    state = simulate_sprint(_parameters(alpha=0, beta=0), 1, 1, 0.5)

    assert state.next_backlog == 0
    assert state.next_debt == 0


@given(
    backlog=st.floats(min_value=0, max_value=1_000, allow_nan=False),
    debt=st.floats(min_value=0, max_value=1_000, allow_nan=False),
    allocation=st.floats(min_value=0, max_value=1, allow_nan=False),
)
def test_sprint_never_returns_negative_states(
    backlog: float, debt: float, allocation: float
) -> None:
    """Preserve non-negative backlog and debt across valid inputs."""
    state = simulate_sprint(_parameters(), backlog, debt, allocation)

    assert state.next_backlog >= 0
    assert state.next_debt >= 0
