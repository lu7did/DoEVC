"""Comparison of remediation policies on equivalent scenarios."""

from collections.abc import Iterable
from dataclasses import dataclass
from statistics import mean

from .models import ModelParameters
from .monte_carlo import MonteCarloRun, run_monte_carlo
from .optimization import Objective
from .policies import Policy
from .simulation import simulate_deterministic_sprints


@dataclass(frozen=True, slots=True)
class PolicyComparison:
    """Metrics and objective value produced by one policy."""

    objective_value: float
    metrics: dict[str, float | dict[str, float]]


def compare_policies(
    parameters: ModelParameters,
    policies: Iterable[Policy],
    objective: Objective,
    *,
    monte_carlo_runs: int | None = None,
    seed: int | None = None,
) -> dict[str, PolicyComparison]:
    """Compare every policy deterministically or through Monte Carlo runs."""
    comparisons: dict[str, PolicyComparison] = {}
    for policy in policies:
        name = type(policy).__name__
        if monte_carlo_runs is None:
            states = simulate_deterministic_sprints(parameters, policy=policy)
            run = MonteCarloRun(parameters, tuple(states))
            comparisons[name] = PolicyComparison(float(objective(states)), run.metrics)
        else:
            result = run_monte_carlo(
                monte_carlo_runs, policy, seed, base_parameters=parameters
            )
            comparisons[name] = PolicyComparison(
                mean(objective(list(run.states)) for run in result.runs),
                result.aggregate_metrics(),
            )
    return comparisons
