"""Policy comparison helpers for deterministic and Monte Carlo evaluation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from statistics import fmean
from typing import Literal

from .models import ModelParameters
from .montecarlo import MetricSummary, aggregate_metrics, run_monte_carlo
from .optimization import ObjectiveFunction
from .policies import Policy
from .sampling import RandomSeed
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

type ComparisonMode = Literal["deterministic", "monte_carlo"]


@dataclass(slots=True, frozen=True)
class DeterministicPolicyComparisonRow:
    """Store the deterministic comparison metrics for one policy."""

    policy_name: str
    convergence_sprints: int
    final_backlog: float
    final_technical_debt: float
    average_remediation_fraction: float
    total_economic_value: float
    completed: bool


@dataclass(slots=True, frozen=True)
class MonteCarloPolicyComparisonRow:
    """Store the Monte Carlo aggregate comparison metrics for one policy."""

    policy_name: str
    n_runs: int
    completed_runs: int
    convergence_sprints: MetricSummary
    final_backlog: MetricSummary
    final_technical_debt: MetricSummary
    average_remediation_fraction: MetricSummary
    total_economic_value: MetricSummary


type PolicyComparisonRow = (
    DeterministicPolicyComparisonRow | MonteCarloPolicyComparisonRow
)


@dataclass(slots=True, frozen=True)
class PolicyComparisonTable:
    """Store the comparison rows produced for one evaluation mode."""

    mode: ComparisonMode
    rows: tuple[PolicyComparisonRow, ...]


def _calculate_average_remediation_fraction(
    trajectory: tuple[SprintState, ...],
) -> float:
    """Calculate the mean remediation fraction for one deterministic run."""
    if not trajectory:
        return 0.0
    return fmean(sprint.remediation_fraction for sprint in trajectory)


def _build_deterministic_row(
    parameters: ModelParameters,
    policy_name: str,
    policy: Policy,
    objective: ObjectiveFunction,
) -> DeterministicPolicyComparisonRow:
    """Build one deterministic comparison row."""
    trajectory = simulate_deterministic_sprints(parameters, policy)
    if trajectory:
        final_backlog = trajectory[-1].next_backlog
        final_technical_debt = trajectory[-1].next_technical_debt
    else:
        final_backlog = parameters.B0
        final_technical_debt = parameters.D0

    return DeterministicPolicyComparisonRow(
        policy_name=policy_name,
        convergence_sprints=len(trajectory),
        final_backlog=final_backlog,
        final_technical_debt=final_technical_debt,
        average_remediation_fraction=_calculate_average_remediation_fraction(
            trajectory
        ),
        total_economic_value=objective(trajectory, parameters),
        completed=final_backlog == 0 and final_technical_debt == 0,
    )


def _build_monte_carlo_row(
    parameters: ModelParameters,
    policy_name: str,
    policy: Policy,
    objective: ObjectiveFunction,
    *,
    n_runs: int,
    seed: RandomSeed,
) -> MonteCarloPolicyComparisonRow:
    """Build one Monte Carlo comparison row using the caller objective."""
    result = run_monte_carlo(
        n_runs,
        policy,
        seed=seed,
        base_parameters=parameters,
    )
    runs = tuple(
        replace(
            run,
            total_economic_value=objective(run.trajectory, run.sampled_parameters),
        )
        for run in result.runs
    )
    aggregate = aggregate_metrics(runs)
    if aggregate.total_economic_value is None:
        raise RuntimeError("aggregate economic value is missing from the comparison.")

    return MonteCarloPolicyComparisonRow(
        policy_name=policy_name,
        n_runs=aggregate.n_runs,
        completed_runs=aggregate.completed_runs,
        convergence_sprints=aggregate.convergence_sprints,
        final_backlog=aggregate.final_backlog,
        final_technical_debt=aggregate.final_technical_debt,
        average_remediation_fraction=aggregate.average_remediation_fraction,
        total_economic_value=aggregate.total_economic_value,
    )


def compare_policies(
    params: ModelParameters,
    policies: Mapping[str, Policy],
    objective: ObjectiveFunction,
    *,
    n_runs: int | None = None,
    seed: RandomSeed = None,
) -> PolicyComparisonTable:
    """Compare multiple policies on the same deterministic or Monte Carlo setup."""
    if not policies:
        raise ValueError("policies must not be empty.")

    if n_runs is None:
        deterministic_rows: tuple[PolicyComparisonRow, ...] = tuple(
            _build_deterministic_row(params, policy_name, policy, objective)
            for policy_name, policy in policies.items()
        )
        return PolicyComparisonTable(mode="deterministic", rows=deterministic_rows)

    monte_carlo_rows: tuple[PolicyComparisonRow, ...] = tuple(
        _build_monte_carlo_row(
            params,
            policy_name,
            policy,
            objective,
            n_runs=n_runs,
            seed=seed,
        )
        for policy_name, policy in policies.items()
    )
    return PolicyComparisonTable(mode="monte_carlo", rows=monte_carlo_rows)
