"""Locally optimized allocation policy."""

from dataclasses import dataclass, replace

from .models import ModelParameters
from .optimization import Objective, find_optimal_allocation
from .sprint import SprintState


@dataclass(frozen=True, slots=True)
class OptimalLocalPolicy:  # pylint: disable=too-few-public-methods
    """Choose the allocation that maximizes an objective from each state."""

    objective: Objective
    step: float = 0.01

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Evaluate the fixed-allocation grid from the current sprint state."""
        current_parameters = replace(params, B0=state.backlog, D0=state.debt)
        return find_optimal_allocation(
            current_parameters,
            self.objective,
            step=self.step,
            maximize=True,
        )
