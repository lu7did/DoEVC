"""Monte Carlo simulation helpers for uncertain model parameters."""

from dataclasses import dataclass
from random import Random

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
class MonteCarloRun:
    """Store the sampled parameters and trajectory of one Monte Carlo run."""

    parameters: ModelParameters
    trajectory: tuple[SprintState, ...]


@dataclass(frozen=True, slots=True)
class MonteCarloSummary:
    """Store aggregate final states from a collection of Monte Carlo runs."""

    run_count: int
    final_backlogs: tuple[float, ...]
    final_technical_debts: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class MonteCarloSimulation:
    """Store individual Monte Carlo runs and their aggregate summary."""

    runs: tuple[MonteCarloRun, ...]
    summary: MonteCarloSummary


def run_monte_carlo(
    n_runs: int,
    policy: Policy,
    seed: int | None,
    *,
    base_parameters: ModelParameters = DEFAULT_MODEL_PARAMETERS,
) -> MonteCarloSimulation:
    """Run reproducible simulations using independently sampled parameters."""
    if n_runs <= 0:
        raise ValueError("n_runs must be greater than zero.")

    # This pseudo-random generator derives reproducible scientific samples.
    generator = Random(seed)  # nosec B311
    runs = tuple(
        _run_sampled_simulation(
            base_parameters,
            policy,
            sample_seed=generator.getrandbits(64),
        )
        for _ in range(n_runs)
    )
    return MonteCarloSimulation(
        runs=runs,
        summary=MonteCarloSummary(
            run_count=n_runs,
            final_backlogs=tuple(run.trajectory[-1].next_backlog for run in runs),
            final_technical_debts=tuple(
                run.trajectory[-1].next_technical_debt for run in runs
            ),
        ),
    )


def _run_sampled_simulation(
    base_parameters: ModelParameters,
    policy: Policy,
    *,
    sample_seed: int,
) -> MonteCarloRun:
    """Sample parameters and execute one deterministic trajectory."""
    parameters = sample_model_parameters(base_parameters, seed=sample_seed)
    return MonteCarloRun(
        parameters=parameters,
        trajectory=simulate_deterministic_sprints(parameters, policy),
    )
