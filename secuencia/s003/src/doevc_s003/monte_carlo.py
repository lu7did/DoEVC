"""Reproducible Monte Carlo execution over sampled model parameters."""

from dataclasses import dataclass
from random import Random
from statistics import pstdev
from typing import Sequence

from .models import ModelParameters
from .policies import Policy
from .sampling import sample_model_parameters
from .simulation import simulate_sprints
from .sprint import SprintState

DEFAULT_PARAMETERS = ModelParameters(
    B0=100,
    D0=20,
    V0=10,
    alpha=0.1,
    beta=0.2,
    gamma=0.01,
    theta=0.5,
    lambda_=0.5,
    rho=0.1,
    K=10,
)


@dataclass(frozen=True, slots=True)
class MonteCarloRun:
    """One sampled parameter set and its simulated trajectory."""

    parameters: ModelParameters
    trajectory: tuple[SprintState, ...]

    @property
    def final_backlog(self) -> float:
        """Return the terminal backlog, including an empty trajectory."""
        return (
            self.trajectory[-1].next_backlog if self.trajectory else self.parameters.B0
        )

    @property
    def final_debt(self) -> float:
        """Return the terminal debt, including an empty trajectory."""
        return self.trajectory[-1].next_debt if self.trajectory else self.parameters.D0

    @property
    def metrics(self) -> "RunMetrics":
        """Calculate the output metrics for this individual run."""
        average_allocation = (
            sum(state.allocation for state in self.trajectory) / len(self.trajectory)
            if self.trajectory
            else 0.0
        )
        return RunMetrics(
            total_sprints=len(self.trajectory),
            final_debt=self.final_debt,
            average_allocation=average_allocation,
            final_backlog=self.final_backlog,
        )


@dataclass(frozen=True, slots=True)
class RunMetrics:
    """Quantitative output metrics for a single Monte Carlo run."""

    total_sprints: int
    final_debt: float
    average_allocation: float
    final_backlog: float


@dataclass(frozen=True, slots=True)
class MetricSummary:
    """Population summary statistics for one output metric."""

    mean: float | None
    standard_deviation: float | None
    minimum: float | None
    maximum: float | None


@dataclass(frozen=True, slots=True)
class AggregateMetrics:
    """Aggregate summaries for every defined Monte Carlo output metric."""

    total_sprints: MetricSummary
    final_debt: MetricSummary
    average_allocation: MetricSummary
    final_backlog: MetricSummary


@dataclass(frozen=True, slots=True)
class MonteCarloResult:
    """Individual Monte Carlo runs and aggregated terminal-state results."""

    runs: tuple[MonteCarloRun, ...]
    mean_final_backlog: float | None
    mean_final_debt: float | None
    metrics: AggregateMetrics


def _summarize(values: Sequence[float]) -> MetricSummary:
    """Calculate population statistics while preserving empty samples."""
    if not values:
        return MetricSummary(None, None, None, None)
    return MetricSummary(
        mean=sum(values) / len(values),
        standard_deviation=pstdev(values),
        minimum=min(values),
        maximum=max(values),
    )


def aggregate_metrics(runs: Sequence[MonteCarloRun]) -> AggregateMetrics:
    """Aggregate all defined output metrics across individual run results."""
    individual_metrics = [run.metrics for run in runs]
    return AggregateMetrics(
        total_sprints=_summarize(
            [float(metrics.total_sprints) for metrics in individual_metrics]
        ),
        final_debt=_summarize([metrics.final_debt for metrics in individual_metrics]),
        average_allocation=_summarize(
            [metrics.average_allocation for metrics in individual_metrics]
        ),
        final_backlog=_summarize(
            [metrics.final_backlog for metrics in individual_metrics]
        ),
    )


def run_monte_carlo(
    n_runs: int,
    policy: Policy,
    seed: int | None,
    template: ModelParameters = DEFAULT_PARAMETERS,
) -> MonteCarloResult:
    """Execute ``n_runs`` sampled simulations using one interchangeable policy."""
    if n_runs < 0:
        raise ValueError("n_runs must not be negative.")

    random_source = Random(seed)
    runs: list[MonteCarloRun] = []
    for _ in range(n_runs):
        parameters = sample_model_parameters(
            template, seed=random_source.randrange(0, 2**63)
        )
        trajectory = tuple(simulate_sprints(parameters, policy))
        runs.append(MonteCarloRun(parameters, trajectory))

    if not runs:
        return MonteCarloResult((), None, None, aggregate_metrics(()))

    aggregate = aggregate_metrics(runs)
    return MonteCarloResult(
        runs=tuple(runs),
        mean_final_backlog=aggregate.final_backlog.mean,
        mean_final_debt=aggregate.final_debt.mean,
        metrics=aggregate,
    )
