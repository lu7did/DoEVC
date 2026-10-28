"""Tests for one-sprint simulation."""

import pytest

from s004 import SprintState, simulate_sprint
from tests.support import create_parameters


def test_simulate_sprint_returns_expected_state() -> None:
    """The simulation follows the specified sprint equations."""
    state = simulate_sprint(
        create_parameters(),
        backlog=100.0,
        technical_debt=20.0,
        remediation_fraction=0.25,
    )

    assert isinstance(state, SprintState)
    assert state.effective_velocity == pytest.approx(6.0)
    assert state.remediation_capacity == pytest.approx(1.5)
    assert state.feature_capacity == pytest.approx(4.5)
    assert state.next_backlog == pytest.approx(95.5)
    assert state.next_technical_debt == pytest.approx(20.0)


@pytest.mark.parametrize("remediation_fraction", [-0.1, 1.1])
def test_simulate_sprint_rejects_fraction_outside_unit_interval(
    remediation_fraction: float,
) -> None:
    """The remediation fraction must remain in the closed unit interval."""
    with pytest.raises(ValueError, match="remediation_fraction must be between"):
        simulate_sprint(
            create_parameters(),
            backlog=100.0,
            technical_debt=20.0,
            remediation_fraction=remediation_fraction,
        )


def test_simulate_sprint_clamps_next_backlog_to_zero() -> None:
    """The next backlog cannot become negative."""
    state = simulate_sprint(
        create_parameters(),
        backlog=1.0,
        technical_debt=0.0,
        remediation_fraction=0.0,
    )

    assert state.next_backlog == 0.0


def test_simulate_sprint_clamps_next_technical_debt_to_zero() -> None:
    """The next technical debt cannot become negative."""
    state = simulate_sprint(
        create_parameters(),
        backlog=100.0,
        technical_debt=0.1,
        remediation_fraction=1.0,
    )

    assert state.next_technical_debt == 0.0
