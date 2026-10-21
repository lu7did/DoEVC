"""Grid-search optimization for fixed remediation allocations."""

from collections.abc import Callable
from math import isclose
from numbers import Real

from .models import ModelParameters
from .simulation import simulate_sprints
from .sprint import SprintState

Objective = Callable[[list[SprintState]], float]


def _grid_values(step: object) -> tuple[float, ...]:
    """Return an inclusive uniform allocation grid from zero through one."""
    if isinstance(step, bool) or not isinstance(step, Real):
        raise TypeError("step must be a real number.")
    step_value = float(step)
    if not 0 < step_value <= 1:
        raise ValueError("step must be greater than zero and at most one.")
    intervals = round(1 / step_value)
    if not isclose(intervals * step_value, 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("step must divide the closed interval from 0 to 1.")
    return tuple(index / intervals for index in range(intervals + 1))


def find_optimal_allocation(
    parameters: ModelParameters,
    objective: Objective,
    *,
    step: float = 0.01,
    maximize: bool = False,
) -> float:
    """Return the fixed allocation that minimizes or maximizes ``objective``."""
    candidates = _grid_values(step)
    best_allocation = candidates[0]
    best_value = objective(simulate_sprints(parameters, best_allocation))

    for allocation in candidates[1:]:
        value = objective(simulate_sprints(parameters, allocation))
        if (maximize and value > best_value) or (not maximize and value < best_value):
            best_allocation = allocation
            best_value = value

    return best_allocation
