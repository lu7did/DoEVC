"""Grid-search optimization helpers for fixed remediation fractions."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from .models import ModelParameters, ensure_non_negative
from .policies import FixedRemediationPolicy
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

type ObjectiveDirection = Literal["min", "max"]
type ObjectiveFunction = Callable[[tuple[SprintState, ...], ModelParameters], float]


@dataclass(slots=True, frozen=True)
class GridSearchEvaluation:
    """Store the objective result for one fixed remediation fraction."""

    remediation_fraction: float
    objective_value: float
    trajectory: tuple[SprintState, ...]


@dataclass(slots=True, frozen=True)
class GridSearchResult:
    """Store all evaluations and the selected optimum from a grid search."""

    best_remediation_fraction: float
    best_objective_value: float
    evaluations: tuple[GridSearchEvaluation, ...]

    @property
    def best_evaluation(self) -> GridSearchEvaluation:
        """Return the selected best evaluation."""
        for evaluation in self.evaluations:
            if evaluation.remediation_fraction == self.best_remediation_fraction:
                return evaluation
        raise RuntimeError("best evaluation is missing from the recorded evaluations.")


def _build_fraction_grid(step: float) -> tuple[float, ...]:
    """Build the remediation grid from 0.0 to 1.0 inclusive."""
    if step <= 0 or step > 1:
        raise ValueError("step must be greater than 0 and at most 1.")

    fractions: list[float] = []
    current = 0.0
    epsilon = step / 1_000
    while current <= 1.0 + epsilon:
        fractions.append(round(min(current, 1.0), 10))
        current += step

    if fractions[-1] != 1.0:
        fractions.append(1.0)

    return tuple(dict.fromkeys(fractions))


def _select_best_evaluation(
    evaluations: tuple[GridSearchEvaluation, ...],
    direction: ObjectiveDirection,
) -> GridSearchEvaluation:
    """Select the best evaluation according to the objective direction."""
    if direction == "min":
        return min(
            evaluations,
            key=lambda evaluation: (
                evaluation.objective_value,
                evaluation.remediation_fraction,
            ),
        )
    return max(
        evaluations,
        key=lambda evaluation: (
            evaluation.objective_value,
            -evaluation.remediation_fraction,
        ),
    )


def search_optimal_remediation_fraction(
    parameters: ModelParameters,
    objective: ObjectiveFunction,
    *,
    direction: ObjectiveDirection = "min",
    step: float = 0.01,
    backlog: float | None = None,
    technical_debt: float | None = None,
) -> GridSearchResult:
    """Evaluate a fixed-``u`` grid and return the remediation fraction that wins."""
    current_backlog = parameters.B0 if backlog is None else backlog
    current_technical_debt = parameters.D0 if technical_debt is None else technical_debt

    ensure_non_negative("backlog", current_backlog)
    ensure_non_negative("technical_debt", current_technical_debt)

    if direction not in {"min", "max"}:
        raise ValueError("direction must be either 'min' or 'max'.")

    if current_technical_debt == 0:
        trajectory = simulate_deterministic_sprints(
            parameters,
            FixedRemediationPolicy(0.0),
            backlog=current_backlog,
            technical_debt=current_technical_debt,
        )
        objective_value = objective(trajectory, parameters)
        evaluation = GridSearchEvaluation(
            remediation_fraction=0.0,
            objective_value=objective_value,
            trajectory=trajectory,
        )
        return GridSearchResult(
            best_remediation_fraction=0.0,
            best_objective_value=objective_value,
            evaluations=(evaluation,),
        )

    evaluations = tuple(
        GridSearchEvaluation(
            remediation_fraction=remediation_fraction,
            objective_value=objective(
                trajectory := simulate_deterministic_sprints(
                    parameters,
                    FixedRemediationPolicy(remediation_fraction),
                    backlog=current_backlog,
                    technical_debt=current_technical_debt,
                ),
                parameters,
            ),
            trajectory=trajectory,
        )
        for remediation_fraction in _build_fraction_grid(step)
    )
    best_evaluation = _select_best_evaluation(evaluations, direction)
    return GridSearchResult(
        best_remediation_fraction=best_evaluation.remediation_fraction,
        best_objective_value=best_evaluation.objective_value,
        evaluations=evaluations,
    )
