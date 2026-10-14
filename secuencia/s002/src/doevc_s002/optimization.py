"""Grid-search optimization for fixed remediation fractions."""

from collections.abc import Callable
from dataclasses import dataclass, replace
from numbers import Real

from .models import ModelParameters
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

Objective = Callable[[list[SprintState]], Real]


@dataclass(frozen=True, slots=True)
class ObjectiveFunction:
    """Economic objective with configurable delivery, debt, and time weights."""

    delivered_value_weight: float = 1.0
    remaining_debt_penalty: float = 1.0
    sprint_penalty: float = 0.0

    def __call__(self, states: list[SprintState]) -> float:
        """Evaluate the economic value of a complete deterministic trajectory."""
        if not states:
            return 0.0
        delivered_value = sum(state.backlog - state.next_backlog for state in states)
        return (
            self.delivered_value_weight * delivered_value
            - self.remaining_debt_penalty * states[-1].next_debt
            - self.sprint_penalty * len(states)
        )


@dataclass(frozen=True, slots=True)
class GridSearchResult:
    """Optimal fixed remediation fraction and all evaluated trajectories."""

    remediation_fraction: float
    objective_value: float
    trajectories: dict[float, tuple[SprintState, ...]]


@dataclass(frozen=True, slots=True)
class OptimalLocalPolicy:
    """Choose the one-sprint remediation fraction with highest objective value."""

    objective: Objective
    step: float = 0.01

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Optimize the next sprint from the current state."""
        local_parameters = replace(params, B0=state.backlog, D0=state.debt, K=1)
        return grid_search_remediation(
            local_parameters, self.objective, step=self.step, maximize=True
        ).remediation_fraction


def grid_search_remediation(
    parameters: ModelParameters,
    objective: Objective,
    *,
    step: float = 0.01,
    maximize: bool = False,
) -> GridSearchResult:
    """Evaluate fixed remediation fractions from zero through one."""
    if not 0 < step <= 1:
        raise ValueError("step must be in the interval (0, 1].")

    points = round(1 / step)
    fractions = [index / points for index in range(points + 1)]
    trajectories = {
        fraction: tuple(simulate_deterministic_sprints(parameters, fraction))
        for fraction in fractions
    }
    values = {
        fraction: float(objective(list(states)))
        for fraction, states in trajectories.items()
    }
    optimal_fraction = (
        max(values, key=values.get) if maximize else min(values, key=values.get)
    )
    return GridSearchResult(optimal_fraction, values[optimal_fraction], trajectories)
