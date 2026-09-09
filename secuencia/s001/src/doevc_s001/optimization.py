"""Grid-search optimization for fixed remediation fractions."""

from collections.abc import Callable
from dataclasses import dataclass
from math import isclose

from .models import ModelParameters
from .policies import Policy
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState


@dataclass(frozen=True, slots=True)
class ObjectiveFunction:
    """Evaluate trajectories using configurable economic value weights."""

    delivered_functionality_weight: float = 1.0
    remaining_debt_penalty: float = 1.0
    sprint_penalty: float = 0.0

    def __call__(self, trajectory: tuple[SprintState, ...]) -> float:
        """Return the weighted economic value of a simulation trajectory."""
        if not trajectory:
            return 0.0

        delivered_functionality = sum(
            state.backlog - state.next_backlog for state in trajectory
        )
        final_technical_debt = trajectory[-1].next_technical_debt
        return (
            self.delivered_functionality_weight * delivered_functionality
            - self.remaining_debt_penalty * final_technical_debt
            - self.sprint_penalty * len(trajectory)
        )


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


@dataclass(frozen=True, slots=True)
class OptimalLocalPolicy(Policy):
    """Select the locally optimal remediation fraction at each sprint."""

    objective: Callable[[tuple[SprintState, ...]], float]
    step: float = 0.01

    def decide_u(self, state: SprintState, params: ModelParameters) -> float:
        """Optimize remediation using the current sprint state as the baseline."""
        result = grid_search_remediation(
            params,
            self.objective,
            step=self.step,
            maximize=True,
            backlog=state.backlog,
            technical_debt=state.technical_debt,
        )
        return result.best_remediation_fraction


def grid_search_remediation(
    parameters: ModelParameters,
    objective: Callable[[tuple[SprintState, ...]], float],
    *,
    step: float = 0.01,
    maximize: bool = False,
    backlog: float | None = None,
    technical_debt: float | None = None,
) -> GridSearchResult:
    """Optimize a fixed remediation fraction over the inclusive unit interval."""
    grid = _build_remediation_grid(step)
    evaluations = tuple(
        _evaluate_remediation_fraction(
            parameters,
            objective,
            remediation_fraction,
            backlog=backlog,
            technical_debt=technical_debt,
        )
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
    objective: Callable[[tuple[SprintState, ...]], float],
    remediation_fraction: float,
    *,
    backlog: float | None,
    technical_debt: float | None,
) -> GridSearchEvaluation:
    """Simulate one fixed fraction and evaluate its resulting trajectory."""
    trajectory = simulate_deterministic_sprints(
        parameters,
        remediation_fraction,
        backlog=backlog,
        technical_debt=technical_debt,
    )
    return GridSearchEvaluation(
        remediation_fraction=remediation_fraction,
        objective_value=objective(trajectory),
        trajectory=trajectory,
    )
