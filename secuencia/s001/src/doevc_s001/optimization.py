"""Grid-search optimization for fixed remediation fractions."""

from collections.abc import Callable
from dataclasses import dataclass
from math import isclose

from .models import ModelParameters
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

ObjectiveFunction = Callable[[tuple[SprintState, ...]], float]


@dataclass(frozen=True, slots=True)
class GridSearchEvaluation:
    """Store one remediation fraction evaluated by the grid search."""

    remediation_fraction: float
    objective_value: float
    trajectory: tuple[SprintState, ...]


@dataclass(frozen=True, slots=True)
class GridSearchResult:
    """Store every grid evaluation and the fraction selected as optimal."""

    best_remediation_fraction: float
    best_objective_value: float
    evaluations: tuple[GridSearchEvaluation, ...]


def grid_search_remediation(
    parameters: ModelParameters,
    objective: ObjectiveFunction,
    *,
    step: float = 0.01,
    maximize: bool = False,
) -> GridSearchResult:
    """Optimize a fixed remediation fraction over the inclusive unit interval."""
    grid = _build_remediation_grid(step)
    evaluations = tuple(
        _evaluate_remediation_fraction(parameters, objective, remediation_fraction)
        for remediation_fraction in grid
    )
    best_evaluation = (
        max(evaluations, key=lambda evaluation: evaluation.objective_value)
        if maximize
        else min(evaluations, key=lambda evaluation: evaluation.objective_value)
    )
    return GridSearchResult(
        best_remediation_fraction=best_evaluation.remediation_fraction,
        best_objective_value=best_evaluation.objective_value,
        evaluations=evaluations,
    )


def _build_remediation_grid(step: float) -> tuple[float, ...]:
    """Build an inclusive uniform grid whose step divides the unit interval."""
    if step <= 0 or step > 1:
        raise ValueError("step must be greater than zero and no greater than one.")

    step_count = round(1 / step)
    if not isclose(step_count * step, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("step must divide the unit interval exactly.")

    return tuple(round(index * step, 12) for index in range(step_count + 1))


def _evaluate_remediation_fraction(
    parameters: ModelParameters,
    objective: ObjectiveFunction,
    remediation_fraction: float,
) -> GridSearchEvaluation:
    """Simulate one fixed fraction and evaluate its resulting trajectory."""
    trajectory = simulate_deterministic_sprints(parameters, remediation_fraction)
    return GridSearchEvaluation(
        remediation_fraction=remediation_fraction,
        objective_value=objective(trajectory),
        trajectory=trajectory,
    )
