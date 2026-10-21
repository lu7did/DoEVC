"""Regression tests for deterministic multi-sprint simulations."""

from doevc_s003 import ModelParameters, simulate_sprints


def _parameters(
    *,
    backlog: float = 10,
    debt: float = 10,
    velocity: float = 4,
    sprints: int = 3,
) -> ModelParameters:
    """Create deterministic scenarios with uncomplicated trajectories."""
    return ModelParameters(backlog, debt, velocity, 0, 0, 0, 0, 0, 0, sprints)


def test_simulation_returns_the_known_fixed_allocation_trajectory() -> None:
    """Chain all requested sprints with the expected state progression."""
    trajectory = simulate_sprints(_parameters(), allocation=0.5)

    assert len(trajectory) == 3
    assert [(state.backlog, state.debt) for state in trajectory] == [
        (10, 10),
        (8, 8),
        (6, 6),
    ]
    assert [
        (state.delivery_capacity, state.remediation_capacity) for state in trajectory
    ] == [
        (2, 2),
        (2, 2),
        (2, 2),
    ]
    assert all(state.velocity == 4 for state in trajectory)
    assert all(state.allocation == 0.5 for state in trajectory)


def test_simulation_stops_when_backlog_and_debt_are_both_zero() -> None:
    """Avoid adding sprints after both state variables are exhausted."""
    trajectory = simulate_sprints(
        _parameters(backlog=2, debt=2, velocity=10, sprints=5), allocation=0.5
    )

    assert len(trajectory) == 1
    assert trajectory[0].next_backlog == 0
    assert trajectory[0].next_debt == 0


def test_simulation_returns_no_sprints_for_an_already_completed_state() -> None:
    """Preserve early termination for a completed initial state."""
    assert simulate_sprints(_parameters(backlog=0, debt=0), allocation=0.5) == []
