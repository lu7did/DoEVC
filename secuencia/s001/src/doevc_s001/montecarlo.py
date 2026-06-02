"""Monte Carlo simulation helpers for DoEVC s001."""

from __future__ import annotations

from dataclasses import dataclass

from .models import ModelParameters
from .policies import Policy
from .sampling import RandomSeed, UniformParameterSampler
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState


@dataclass(slots=True, frozen=True)
class MonteCarloRunResult:
    """Store the sampled parameters and deterministic trajectory of one run."""

    run_index: int
    sampled_parameters: ModelParameters
    trajectory: tuple[SprintState, ...]
    executed_sprints: int
    final_backlog: float
    final_technical_debt: float
    completed: bool

    def to_dict(self) -> dict[str, int | float | bool | dict[str, float | int]]:
        """Serialize the run result to a dictionary."""
        return {
            "run_index": self.run_index,
            "sampled_parameters": self.sampled_parameters.to_dict(),
            "executed_sprints": self.executed_sprints,
            "final_backlog": self.final_backlog,
            "final_technical_debt": self.final_technical_debt,
            "completed": self.completed,
        }


@dataclass(slots=True, frozen=True)
class MonteCarloAggregateResult:
    """Store the aggregate Monte Carlo statistics across all runs."""

    n_runs: int
    completed_runs: int
    mean_final_backlog: float
    mean_final_technical_debt: float
    mean_executed_sprints: float

    def to_dict(self) -> dict[str, int | float]:
        """Serialize the aggregate result to a dictionary."""
        return {
            "n_runs": self.n_runs,
            "completed_runs": self.completed_runs,
            "mean_final_backlog": self.mean_final_backlog,
            "mean_final_technical_debt": self.mean_final_technical_debt,
            "mean_executed_sprints": self.mean_executed_sprints,
        }


@dataclass(slots=True, frozen=True)
class MonteCarloResult:
    """Store the individual and aggregate results of a Monte Carlo execution."""

    runs: tuple[MonteCarloRunResult, ...]
    aggregate: MonteCarloAggregateResult


def _build_run_result(
    run_index: int,
    sampled_parameters: ModelParameters,
    trajectory: tuple[SprintState, ...],
) -> MonteCarloRunResult:
    """Build the run result structure from one deterministic trajectory."""
    if trajectory:
        final_backlog = trajectory[-1].next_backlog
        final_technical_debt = trajectory[-1].next_technical_debt
    else:
        final_backlog = sampled_parameters.B0
        final_technical_debt = sampled_parameters.D0

    return MonteCarloRunResult(
        run_index=run_index,
        sampled_parameters=sampled_parameters,
        trajectory=trajectory,
        executed_sprints=len(trajectory),
        final_backlog=final_backlog,
        final_technical_debt=final_technical_debt,
        completed=final_backlog == 0 and final_technical_debt == 0,
    )


def _aggregate_runs(runs: tuple[MonteCarloRunResult, ...]) -> MonteCarloAggregateResult:
    """Calculate aggregate results across all Monte Carlo runs."""
    run_count = len(runs)
    completed_runs = sum(1 for run in runs if run.completed)
    return MonteCarloAggregateResult(
        n_runs=run_count,
        completed_runs=completed_runs,
        mean_final_backlog=sum(run.final_backlog for run in runs) / run_count,
        mean_final_technical_debt=(
            sum(run.final_technical_debt for run in runs) / run_count
        ),
        mean_executed_sprints=sum(run.executed_sprints for run in runs) / run_count,
    )


def run_monte_carlo(
    n_runs: int,
    policy: Policy,
    seed: RandomSeed = None,
    *,
    base_parameters: ModelParameters,
) -> MonteCarloResult:
    """Execute ``n_runs`` deterministic simulations using C1 parameter sampling."""
    if n_runs <= 0:
        raise ValueError("n_runs must be greater than zero.")

    sampler = UniformParameterSampler(base_parameters=base_parameters, seed=seed)
    runs = tuple(
        _build_run_result(
            run_index=run_index,
            sampled_parameters=sampled_parameters,
            trajectory=simulate_deterministic_sprints(sampled_parameters, policy),
        )
        for run_index, sampled_parameters in enumerate(
            (sampler.sample() for _ in range(n_runs)),
            start=1,
        )
    )
    return MonteCarloResult(runs=runs, aggregate=_aggregate_runs(runs))
