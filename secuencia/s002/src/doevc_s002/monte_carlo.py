"""Monte Carlo execution for uncertain deterministic simulations."""

from dataclasses import dataclass
from random import Random
from statistics import mean, pstdev

from .models import ModelParameters
from .policies import Policy
from .sampling import sample_model_parameters
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState


@dataclass(frozen=True, slots=True)
class MonteCarloRun:
    """Parameters and trajectory produced by one simulation run."""

    parameters: ModelParameters
    states: tuple[SprintState, ...]

    @property
    def metrics(self) -> dict[str, float]:
        """Return quantitative metrics for this trajectory."""
        final_state = self.states[-1] if self.states else None
        return {
            "sprints": float(len(self.states)),
            "final_debt": final_state.next_debt if final_state else self.parameters.D0,
            "mean_remediation": (
                mean(state.remediation_fraction for state in self.states)
                if self.states
                else 0.0
            ),
            "final_backlog": (
                final_state.next_backlog if final_state else self.parameters.B0
            ),
        }


@dataclass(frozen=True, slots=True)
class MonteCarloResult:
    """Individual trajectories and aggregate run count."""

    runs: tuple[MonteCarloRun, ...]

    @property
    def n_runs(self) -> int:
        """Return the number of completed simulations."""
        return len(self.runs)

    def aggregate_metrics(self) -> dict[str, dict[str, float]]:
        """Calculate mean, population deviation, minimum, and maximum per metric."""
        if not self.runs:
            return {}
        return {
            name: {
                "mean": mean(values),
                "stddev": pstdev(values),
                "min": min(values),
                "max": max(values),
            }
            for name in self.runs[0].metrics
            for values in [[run.metrics[name] for run in self.runs]]
        }


def run_monte_carlo(
    n_runs: int, policy: Policy, seed: int | None = None
) -> MonteCarloResult:
    """Execute reproducible simulations using independently sampled parameters."""
    if isinstance(n_runs, bool) or not isinstance(n_runs, int):
        raise TypeError("n_runs must be an integer.")
    if n_runs < 0:
        raise ValueError("n_runs must be non-negative.")

    random = Random(seed)
    base_parameters = ModelParameters(100, 20, 10, 0.1, 0.2, 0.01, 0.3, 0.5, 0.4, 12)
    runs = tuple(
        MonteCarloRun(
            parameters := sample_model_parameters(
                base_parameters, random.randrange(2**32)
            ),
            tuple(simulate_deterministic_sprints(parameters, policy=policy)),
        )
        for _ in range(n_runs)
    )
    return MonteCarloResult(runs)
