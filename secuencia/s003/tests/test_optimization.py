"""Regression tests for fixed-allocation grid search in s003."""

from doevc_s003 import ModelParameters, find_optimal_allocation
from doevc_s003.sprint import SprintState


def _parameters() -> ModelParameters:
    """Create a one-sprint scenario with opposite backlog objectives."""
    return ModelParameters(10, 0, 10, 0, 0, 0, 0, 0, 0, 1)


def _final_backlog(trajectory: list[SprintState]) -> float:
    """Return the final backlog for a guaranteed non-empty trajectory."""
    return trajectory[-1].next_backlog


def test_grid_search_finds_the_allocation_that_minimizes_final_backlog() -> None:
    """Prefer full delivery when the objective is terminal backlog."""
    optimal_allocation = find_optimal_allocation(
        _parameters(), _final_backlog, step=0.25
    )

    assert optimal_allocation == 0


def test_grid_search_can_maximize_a_configurable_objective() -> None:
    """Prefer full remediation when maximizing terminal backlog."""
    optimal_allocation = find_optimal_allocation(
        _parameters(), _final_backlog, step=0.25, maximize=True
    )

    assert optimal_allocation == 1


def test_grid_search_evaluates_every_inclusive_grid_value() -> None:
    """Run one complete deterministic simulation for each configured value."""
    evaluated_allocations: list[float] = []

    def record_allocation(trajectory: list[SprintState]) -> float:
        """Record the fixed allocation supplied to this simulation."""
        evaluated_allocations.append(trajectory[0].allocation)
        return 0

    find_optimal_allocation(_parameters(), record_allocation, step=0.25)

    assert evaluated_allocations == [0, 0.25, 0.5, 0.75, 1]
