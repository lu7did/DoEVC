"""Grid-search optimization for fixed remediation fractions."""

from collections.abc import Callable
from dataclasses import dataclass
from numbers import Real

from .models import ModelParameters
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

Objective = Callable[[list[SprintState]], Real]


@dataclass(frozen=True, slots=True)
class GridSearchResult:
    """Optimal fixed remediation fraction and all evaluated trajectories."""

    remediation_fraction: float
    objective_value: float
    trajectories: dict[float, tuple[SprintState, ...]]


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
