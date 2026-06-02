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


def _calculate_delivered_functionality(trajectory: tuple[SprintState, ...]) -> float:
    """Calculate realized delivered functionality across the trajectory."""
    return sum(min(state.backlog, state.feature_capacity) for state in trajectory)


@dataclass(slots=True, frozen=True)
class EconomicObjectiveFunction:
    """Score a trajectory using configurable economic weights."""

    delivered_value_weight: float = 1.0
    residual_debt_penalty_weight: float = 1.0
    sprint_penalty_weight: float = 0.0

    def __post_init__(self) -> None:
        """Validate the configured economic weights."""
        ensure_non_negative("delivered_value_weight", self.delivered_value_weight)
        ensure_non_negative(
            "residual_debt_penalty_weight",
            self.residual_debt_penalty_weight,
        )
        ensure_non_negative("sprint_penalty_weight", self.sprint_penalty_weight)

    def __call__(
        self,
        trajectory: tuple[SprintState, ...],
        parameters: ModelParameters,
    ) -> float:
        """Evaluate the configured economic objective on one trajectory."""
        delivered_value = (
            self.delivered_value_weight
            * parameters.lambda_
            * _calculate_delivered_functionality(trajectory)
        )
        residual_debt = (
            parameters.D0 if not trajectory else trajectory[-1].next_technical_debt
        )
        debt_penalty = (
            self.residual_debt_penalty_weight * parameters.rho * residual_debt
        )
        sprint_penalty = self.sprint_penalty_weight * parameters.theta * len(trajectory)
        return delivered_value - debt_penalty - sprint_penalty


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
