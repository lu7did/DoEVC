"""Monte Carlo simulations with sampled model parameters."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from random import Random
from statistics import fmean, pstdev

from .models import ModelParameters
from .policies import Policy
from .sampling import sample_model_parameters
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

DEFAULT_MODEL_PARAMETERS = ModelParameters(
    B0=100.0,
    D0=20.0,
    V0=12.0,
    alpha=0.3,
    beta=0.1,
    gamma=0.05,
    theta=0.2,
    lambda_=0.8,
    rho=0.4,
    K=16,
)


@dataclass(frozen=True, slots=True)
class MonteCarloResult:
    """Store output metrics calculated from one Monte Carlo trajectory."""

    sprint_count: int
    final_technical_debt: float
    mean_remediation_fraction: float
    final_backlog: float


@dataclass(frozen=True, slots=True)
class MonteCarloRun:
    """Store sampled parameters, trajectory, and metrics for one run."""

    parameters: ModelParameters
    trajectory: tuple[SprintState, ...]
    metrics: MonteCarloResult


@dataclass(frozen=True, slots=True)
class MetricSummary:
    """Store descriptive statistics for a metric across all runs."""

    mean: float
    standard_deviation: float
    minimum: float
    maximum: float


@dataclass(frozen=True, slots=True)
class MonteCarloSummary:
    """Store aggregate final states from a Monte Carlo batch."""

    run_count: int
    final_backlogs: tuple[float, ...]
    final_technical_debts: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class MonteCarloSimulation:
    """Store individual runs and their aggregate results."""

    runs: tuple[MonteCarloRun, ...]
    summary: MonteCarloSummary
    metrics: dict[str, MetricSummary]


def run_monte_carlo(
    n_runs: int,
    policy: Policy,
    seed: int | None,
    *,
    base_parameters: ModelParameters = DEFAULT_MODEL_PARAMETERS,
) -> MonteCarloSimulation:
    """Run reproducible simulations using independently sampled parameters."""
    if isinstance(n_runs, bool) or not isinstance(n_runs, int) or n_runs <= 0:
        raise ValueError("n_runs must be greater than zero.")

    generator = Random(seed)  # nosec B311
    runs = tuple(
        _run_sampled_simulation(
            base_parameters,
            policy,
            sample_seed=generator.getrandbits(64),
        )
        for _ in range(n_runs)
    )
    run_metrics = tuple(run.metrics for run in runs)
    return MonteCarloSimulation(
        runs=runs,
        summary=MonteCarloSummary(
            run_count=n_runs,
            final_backlogs=tuple(metric.final_backlog for metric in run_metrics),
            final_technical_debts=tuple(
                metric.final_technical_debt for metric in run_metrics
            ),
        ),
        metrics=aggregate_metrics(run_metrics),
    )


def _run_sampled_simulation(
    base_parameters: ModelParameters,
    policy: Policy,
    *,
    sample_seed: int,
) -> MonteCarloRun:
    """Sample parameters and execute their deterministic trajectory."""
    parameters = sample_model_parameters(base_parameters, seed=sample_seed)
    trajectory = simulate_deterministic_sprints(parameters, policy)
    return MonteCarloRun(
        parameters=parameters,
        trajectory=trajectory,
        metrics=calculate_run_metrics(trajectory),
    )


def calculate_run_metrics(
    trajectory: tuple[SprintState, ...],
) -> MonteCarloResult:
    """Calculate the output metrics for one simulation trajectory."""
    if not trajectory:
        return MonteCarloResult(0, 0.0, 0.0, 0.0)

    final_state = trajectory[-1]
    return MonteCarloResult(
        sprint_count=len(trajectory),
        final_technical_debt=final_state.next_technical_debt,
        mean_remediation_fraction=fmean(
            state.remediation_fraction for state in trajectory
        ),
        final_backlog=final_state.next_backlog,
    )


def aggregate_metrics(
    results: Sequence[MonteCarloResult],
) -> dict[str, MetricSummary]:
    """Calculate population statistics for each output metric."""
    if not results:
        raise ValueError("results must contain at least one Monte Carlo result.")

    return {
        "sprint_count": _summarize(result.sprint_count for result in results),
        "final_technical_debt": _summarize(
            result.final_technical_debt for result in results
        ),
        "mean_remediation_fraction": _summarize(
            result.mean_remediation_fraction for result in results
        ),
        "final_backlog": _summarize(result.final_backlog for result in results),
    }


def _summarize(values: Iterable[float]) -> MetricSummary:
    """Calculate descriptive population statistics for non-empty values."""
    metric_values = tuple(values)
    return MetricSummary(
        mean=fmean(metric_values),
        standard_deviation=pstdev(metric_values),
        minimum=min(metric_values),
        maximum=max(metric_values),
    )
