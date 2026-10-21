"""Comparable deterministic and Monte Carlo policy evaluations."""

from collections.abc import Mapping
from dataclasses import dataclass

from .models import ModelParameters
from .monte_carlo import (
    MonteCarloResult,
    MonteCarloRun,
    aggregate_metrics,
    run_monte_carlo,
)
from .optimization import Objective
from .policies import Policy
from .simulation import simulate_sprints


@dataclass(frozen=True, slots=True)
class PolicyComparison:
    """Metrics and mean objective value for one evaluated policy."""

    name: str
    result: MonteCarloResult
    objective_mean: float


@dataclass(frozen=True, slots=True)
class PolicyComparisonTable:
    """One comparable row per policy evaluated on an equivalent scenario."""

    rows: tuple[PolicyComparison, ...]


def _deterministic_result(
    parameters: ModelParameters, policy: Policy
) -> MonteCarloResult:
    """Adapt one deterministic trajectory to the common C3 result structure."""
    run = MonteCarloRun(parameters, tuple(simulate_sprints(parameters, policy)))
    metrics = aggregate_metrics((run,))
    return MonteCarloResult(
        runs=(run,),
        mean_final_backlog=metrics.final_backlog.mean,
        mean_final_debt=metrics.final_debt.mean,
        metrics=metrics,
    )


def compare_policies(
    parameters: ModelParameters,
    policies: Mapping[str, Policy],
    objective: Objective,
    *,
    n_runs: int = 1,
    seed: int | None = None,
) -> PolicyComparisonTable:
    """Compare named policies deterministically or through Monte Carlo runs."""
    if n_runs < 1:
        raise ValueError("n_runs must be at least one.")

    rows: list[PolicyComparison] = []
    for name, policy in policies.items():
        result = (
            _deterministic_result(parameters, policy)
            if n_runs == 1
            else run_monte_carlo(n_runs, policy, seed, parameters)
        )
        objective_mean = sum(
            objective(list(run.trajectory)) for run in result.runs
        ) / len(result.runs)
        rows.append(PolicyComparison(name, result, objective_mean))

    return PolicyComparisonTable(tuple(rows))
