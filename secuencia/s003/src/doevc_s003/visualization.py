"""Non-interactive visualizations for deterministic simulations."""

# pyright: reportUnknownMemberType=false
# pylint: disable=wrong-import-position

from collections.abc import Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot as plt

from .monte_carlo import MonteCarloResult, RunMetrics
from .sprint import SprintState


def plot_simulation(states: Sequence[SprintState], filepath: str | Path) -> None:
    """Plot backlog and technical debt by sprint into a PNG file."""
    sprint_indexes = list(range(len(states)))
    figure, axes = plt.subplots()
    axes.plot(sprint_indexes, [state.backlog for state in states], label="B_k")
    axes.plot(sprint_indexes, [state.debt for state in states], label="D_k")
    axes.set_xlabel("Sprint")
    axes.set_ylabel("Work")
    axes.set_title("Backlog and technical debt by sprint")
    axes.legend()
    axes.grid()
    figure.tight_layout()
    figure.savefig(Path(filepath), format="png")
    plt.close(figure)


def plot_optimal_u_distribution(
    results: MonteCarloResult | Sequence[RunMetrics], filepath: str | Path
) -> None:
    """Plot the per-run optimal-allocation summaries as a PNG boxplot."""
    metrics = (
        [run.metrics for run in results.runs]
        if isinstance(results, MonteCarloResult)
        else results
    )
    allocations = [metric.average_allocation for metric in metrics]
    if not allocations:
        raise ValueError("results must contain at least one run metric.")

    figure, axes = plt.subplots()
    axes.boxplot(allocations)
    axes.set_xlabel("Monte Carlo runs")
    axes.set_ylabel("Average optimal u_k")
    axes.set_title("Distribution of optimal remediation allocation")
    axes.grid(axis="y")
    figure.tight_layout()
    figure.savefig(Path(filepath), format="png")
    plt.close(figure)
