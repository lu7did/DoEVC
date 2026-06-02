"""Monte Carlo simulation helpers for DoEVC s001."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from statistics import fmean, pstdev

from .models import ModelParameters
from .optimization import EconomicObjectiveFunction
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
    convergence_sprints: int
    final_backlog: float
    final_technical_debt: float
    average_remediation_fraction: float
    total_economic_value: float | None
    completed: bool

    @property
    def executed_sprints(self) -> int:
        """Return the executed sprint count for backward compatibility."""
        return self.convergence_sprints

    def to_dict(
        self,
    ) -> dict[str, int | float | bool | None | dict[str, float | int]]:
        """Serialize the run result to a dictionary."""
        return {
            "run_index": self.run_index,
            "sampled_parameters": self.sampled_parameters.to_dict(),
            "convergence_sprints": self.convergence_sprints,
            "executed_sprints": self.executed_sprints,
            "final_backlog": self.final_backlog,
            "final_technical_debt": self.final_technical_debt,
            "average_remediation_fraction": self.average_remediation_fraction,
            "total_economic_value": self.total_economic_value,
            "completed": self.completed,
        }


@dataclass(slots=True, frozen=True)
class MetricSummary:
    """Store summary statistics for one Monte Carlo metric."""

    mean: float
    standard_deviation: float
    minimum: float
    maximum: float
    percentile_25: float
    percentile_50: float
    percentile_75: float

    def to_dict(self) -> dict[str, float]:
        """Serialize the metric summary to a dictionary."""
        return {
            "mean": self.mean,
            "standard_deviation": self.standard_deviation,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "percentile_25": self.percentile_25,
            "percentile_50": self.percentile_50,
            "percentile_75": self.percentile_75,
        }


@dataclass(slots=True, frozen=True)
class MonteCarloAggregateResult:
    """Store the aggregate Monte Carlo statistics across all runs."""

    n_runs: int
    completed_runs: int
    convergence_sprints: MetricSummary
    final_backlog: MetricSummary
    final_technical_debt: MetricSummary
    average_remediation_fraction: MetricSummary
    total_economic_value: MetricSummary | None

    @property
    def mean_final_backlog(self) -> float:
        """Return the mean final backlog for backward compatibility."""
        return self.final_backlog.mean

    @property
    def mean_final_technical_debt(self) -> float:
        """Return the mean final technical debt for backward compatibility."""
        return self.final_technical_debt.mean

    @property
    def mean_executed_sprints(self) -> float:
        """Return the mean convergence sprint count for backward compatibility."""
        return self.convergence_sprints.mean

    def to_dict(self) -> dict[str, int | dict[str, float] | None]:
        """Serialize the aggregate result to a dictionary."""
        return {
            "n_runs": self.n_runs,
            "completed_runs": self.completed_runs,
            "convergence_sprints": self.convergence_sprints.to_dict(),
            "final_backlog": self.final_backlog.to_dict(),
            "final_technical_debt": self.final_technical_debt.to_dict(),
            "average_remediation_fraction": (
                self.average_remediation_fraction.to_dict()
            ),
            "total_economic_value": (
                None
                if self.total_economic_value is None
                else self.total_economic_value.to_dict()
            ),
        }


@dataclass(slots=True, frozen=True)
class MonteCarloResult:
    """Store the individual and aggregate results of a Monte Carlo execution."""

    runs: tuple[MonteCarloRunResult, ...]
    aggregate: MonteCarloAggregateResult


def _calculate_average_remediation_fraction(
    trajectory: tuple[SprintState, ...],
) -> float:
    """Calculate the mean remediation fraction for one run."""
    if not trajectory:
        return 0.0
    return fmean(sprint.remediation_fraction for sprint in trajectory)


def _calculate_total_economic_value(
    parameters: ModelParameters,
    trajectory: tuple[SprintState, ...],
) -> float | None:
    """Return the total economic value when the model defines it."""
    return EconomicObjectiveFunction()(trajectory, parameters)


def _percentile(values: tuple[float, ...], percentile: float) -> float:
    """Calculate one percentile using linear interpolation."""
    if not values:
        raise ValueError("values must not be empty.")

    ordered_values = tuple(sorted(values))
    if len(ordered_values) == 1:
        return ordered_values[0]

    position = (len(ordered_values) - 1) * percentile
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(ordered_values) - 1)
    weight = position - lower_index
    lower_value = ordered_values[lower_index]
    upper_value = ordered_values[upper_index]
    return lower_value + (upper_value - lower_value) * weight


def _summarize_metric(values: tuple[float, ...]) -> MetricSummary:
    """Build a metric summary using population statistics."""
    return MetricSummary(
        mean=fmean(values),
        standard_deviation=0.0 if len(values) == 1 else pstdev(values),
        minimum=min(values),
        maximum=max(values),
        percentile_25=_percentile(values, 0.25),
        percentile_50=_percentile(values, 0.50),
        percentile_75=_percentile(values, 0.75),
    )


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
        convergence_sprints=len(trajectory),
        final_backlog=final_backlog,
        final_technical_debt=final_technical_debt,
        average_remediation_fraction=_calculate_average_remediation_fraction(
            trajectory
        ),
        total_economic_value=_calculate_total_economic_value(
            sampled_parameters,
            trajectory,
        ),
        completed=final_backlog == 0 and final_technical_debt == 0,
    )


def aggregate_metrics(
    runs: tuple[MonteCarloRunResult, ...],
) -> MonteCarloAggregateResult:
    """Calculate aggregate metric summaries across all Monte Carlo runs."""
    if not runs:
        raise ValueError("runs must not be empty.")

    run_count = len(runs)
    completed_runs = sum(1 for run in runs if run.completed)
    economic_values = tuple(
        run.total_economic_value for run in runs if run.total_economic_value is not None
    )
    return MonteCarloAggregateResult(
        n_runs=run_count,
        completed_runs=completed_runs,
        convergence_sprints=_summarize_metric(
            tuple(float(run.convergence_sprints) for run in runs)
        ),
        final_backlog=_summarize_metric(tuple(run.final_backlog for run in runs)),
        final_technical_debt=_summarize_metric(
            tuple(run.final_technical_debt for run in runs)
        ),
        average_remediation_fraction=_summarize_metric(
            tuple(run.average_remediation_fraction for run in runs)
        ),
        total_economic_value=(
            None
            if len(economic_values) != run_count
            else _summarize_metric(tuple(economic_values))
        ),
    )


def export_monte_carlo_metrics_csv(
    result: MonteCarloResult,
    destination: str | PathLike[str],
) -> Path:
    """Export per-run Monte Carlo metrics to CSV with stable columns."""
    destination_path = Path(destination)
    fieldnames = (
        "run_index",
        "convergence_sprints",
        "final_backlog",
        "final_technical_debt",
        "average_remediation_fraction",
        "total_economic_value",
        "completed",
    )
    with destination_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for run in result.runs:
            writer.writerow(
                {
                    "run_index": run.run_index,
                    "convergence_sprints": run.convergence_sprints,
                    "final_backlog": run.final_backlog,
                    "final_technical_debt": run.final_technical_debt,
                    "average_remediation_fraction": run.average_remediation_fraction,
                    "total_economic_value": (
                        ""
                        if run.total_economic_value is None
                        else run.total_economic_value
                    ),
                    "completed": run.completed,
                }
            )
    return destination_path


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
    return MonteCarloResult(runs=runs, aggregate=aggregate_metrics(runs))
