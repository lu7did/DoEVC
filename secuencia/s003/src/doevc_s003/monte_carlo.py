"""Reproducible Monte Carlo execution over sampled model parameters."""

from dataclasses import dataclass
from random import Random

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


@dataclass(frozen=True, slots=True)
class MonteCarloResult:
    """Individual Monte Carlo runs and aggregated terminal-state results."""

    runs: tuple[MonteCarloRun, ...]
    mean_final_backlog: float | None
    mean_final_debt: float | None


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
        return MonteCarloResult((), None, None)

    return MonteCarloResult(
        runs=tuple(runs),
        mean_final_backlog=sum(run.final_backlog for run in runs) / len(runs),
        mean_final_debt=sum(run.final_debt for run in runs) / len(runs),
    )
