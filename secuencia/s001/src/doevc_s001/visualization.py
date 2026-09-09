"""Non-interactive visualizations for deterministic simulations."""

# pyright: reportUnknownMemberType=false

from collections.abc import Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from .monte_carlo import MonteCarloResult, MonteCarloSimulation
from .sprint import SprintState


def plot_simulation(states: Sequence[SprintState], filepath: str | Path) -> None:
    """Render backlog and technical debt by sprint to a PNG file."""
    sprints = range(1, len(states) + 1)
    figure, axis = plt.subplots()
    axis.plot(sprints, tuple(state.backlog for state in states), label="B_k")
    axis.plot(sprints, tuple(state.technical_debt for state in states), label="D_k")
    axis.set_xlabel("Sprint")
    axis.set_ylabel("Work")
    axis.legend()
    figure.tight_layout()
    figure.savefig(filepath, format="png")
    plt.close(figure)


def plot_optimal_u_distribution(
    results: Sequence[MonteCarloResult] | MonteCarloSimulation,
    filepath: str | Path,
) -> None:
    """Render a boxplot of mean remediation fractions from Monte Carlo runs."""
    remediation_fractions = _mean_remediation_fractions(results)
    if not remediation_fractions:
        raise ValueError("results must contain at least one Monte Carlo result.")

    figure, axis = plt.subplots()
    axis.boxplot(remediation_fractions)
    axis.set_ylabel("Mean u_k")
    figure.tight_layout()
    figure.savefig(filepath, format="png")
    plt.close(figure)


def _mean_remediation_fractions(
    results: Sequence[MonteCarloResult] | MonteCarloSimulation,
) -> tuple[float, ...]:
    """Extract one remediation metric from each Monte Carlo run."""
    if isinstance(results, MonteCarloSimulation):
        return tuple(run.metrics.mean_remediation_fraction for run in results.runs)
    return tuple(result.mean_remediation_fraction for result in results)
