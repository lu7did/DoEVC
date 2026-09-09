"""Comparison helpers for remediation policies."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from statistics import fmean

from .models import ModelParameters
from .monte_carlo import (
    MetricSummary,
    MonteCarloSimulation,
    aggregate_metrics,
    calculate_run_metrics,
    run_monte_carlo,
)
from .policies import Policy
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState


@dataclass(frozen=True, slots=True)
class MonteCarloComparisonConfig:
    """Configure reproducible Monte Carlo policy comparisons."""

    n_runs: int
    seed: int | None
    base_parameters: ModelParameters


@dataclass(frozen=True, slots=True)
class PolicyComparison:
    """Store one row of a deterministic or Monte Carlo policy comparison."""

    name: str
    objective_value: float
    metrics: dict[str, MetricSummary]
    deterministic_trajectory: tuple[SprintState, ...] | None = None
    monte_carlo_simulation: MonteCarloSimulation | None = None


def compare_policies(
    parameters: ModelParameters | MonteCarloComparisonConfig,
    policies: Mapping[str, Policy],
    objective: Callable[[tuple[SprintState, ...]], float],
) -> tuple[PolicyComparison, ...]:
    """Evaluate each named policy under the same deterministic or random scenario."""
    if not policies:
        raise ValueError("policies must contain at least one policy.")

    if isinstance(parameters, MonteCarloComparisonConfig):
        return tuple(
            _compare_monte_carlo_policy(parameters, name, policy, objective)
            for name, policy in policies.items()
        )
    return tuple(
        _compare_deterministic_policy(parameters, name, policy, objective)
        for name, policy in policies.items()
    )


def _compare_deterministic_policy(
    parameters: ModelParameters,
    name: str,
    policy: Policy,
    objective: Callable[[tuple[SprintState, ...]], float],
) -> PolicyComparison:
    """Build one comparison row from a deterministic trajectory."""
    trajectory = simulate_deterministic_sprints(parameters, policy)
    metrics = aggregate_metrics((calculate_run_metrics(trajectory),))
    return PolicyComparison(
        name=name,
        objective_value=objective(trajectory),
        metrics=metrics,
        deterministic_trajectory=trajectory,
    )


def _compare_monte_carlo_policy(
    config: MonteCarloComparisonConfig,
    name: str,
    policy: Policy,
    objective: Callable[[tuple[SprintState, ...]], float],
) -> PolicyComparison:
    """Build one comparison row from reproducible Monte Carlo simulations."""
    simulation = run_monte_carlo(
        config.n_runs,
        policy,
        config.seed,
        base_parameters=config.base_parameters,
    )
    return PolicyComparison(
        name=name,
        objective_value=fmean(objective(run.trajectory) for run in simulation.runs),
        metrics=simulation.metrics,
        monte_carlo_simulation=simulation,
    )
