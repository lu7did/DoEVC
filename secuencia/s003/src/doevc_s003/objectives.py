"""Configurable economic objectives for simulation trajectories."""

from dataclasses import dataclass

from .sprint import SprintState


@dataclass(frozen=True, slots=True)
class EconomicObjective:
    """Value delivered functionality while penalizing debt and elapsed sprints."""

    delivery_weight: float = 1.0
    debt_weight: float = 1.0
    sprint_weight: float = 0.0

    def __call__(self, trajectory: list[SprintState]) -> float:
        """Evaluate a trajectory for compatibility with grid-search objectives."""
        delivered_value = sum(
            state.backlog - state.next_backlog for state in trajectory
        )
        final_debt = trajectory[-1].next_debt if trajectory else 0.0
        return (
            self.delivery_weight * delivered_value
            - self.debt_weight * final_debt
            - self.sprint_weight * len(trajectory)
        )
