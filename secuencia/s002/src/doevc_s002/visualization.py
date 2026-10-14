"""Non-interactive visualizations for deterministic simulations."""

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot as plt

from .models import ModelParameters
from .monte_carlo import MonteCarloResult
from .policies import Policy
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState


def plot_simulation(states: Iterable[SprintState], filepath: str | Path) -> None:
    """Save backlog and debt values across sprint indices as a PNG."""
    trajectory = list(states)
    sprints = range(1, len(trajectory) + 1)
    figure, axis = plt.subplots()
    axis.plot(sprints, [state.backlog for state in trajectory], label="Backlog")
    axis.plot(sprints, [state.debt for state in trajectory], label="Technical debt")
    axis.set_xlabel("Sprint")
    axis.set_ylabel("Work")
    axis.legend()
    figure.tight_layout()
    figure.savefig(filepath, format="png")
    plt.close(figure)


def plot_sensitivity_heatmap(
    param1_range: tuple[str, Sequence[float]],
    param2_range: tuple[str, Sequence[float]],
    base_parameters: ModelParameters,
    policy: Policy,
    filepath: str | Path,
) -> list[list[float]]:
    """Save and return mean-remediation sensitivity across two parameters."""
    parameter1, values1 = param1_range
    parameter2, values2 = param2_range
    if not hasattr(base_parameters, parameter1) or not hasattr(
        base_parameters, parameter2
    ):
        raise ValueError("Sensitivity parameters must be ModelParameters fields.")
    if not values1 or not values2:
        raise ValueError("Sensitivity ranges must not be empty.")

    matrix = [
        [
            mean(
                state.remediation_fraction
                for state in simulate_deterministic_sprints(
                    replace(
                        replace(base_parameters, **{parameter1: value1}),
                        **{parameter2: value2},
                    ),
                    policy=policy,
                )
            )
            for value1 in values1
        ]
        for value2 in values2
    ]
    figure, axis = plt.subplots()
    image = axis.imshow(matrix, origin="lower", aspect="auto")
    axis.set_xticks(range(len(values1)), labels=[str(value) for value in values1])
    axis.set_yticks(range(len(values2)), labels=[str(value) for value in values2])
    axis.set_xlabel(parameter1)
    axis.set_ylabel(parameter2)
    figure.colorbar(image, ax=axis, label="Mean remediation fraction")
    figure.tight_layout()
    figure.savefig(filepath, format="png")
    plt.close(figure)
    return matrix


def plot_optimal_u_distribution(
    results: MonteCarloResult | Iterable[Mapping[str, float]],
    filepath: str | Path,
) -> None:
    """Save a boxplot of per-run remediation values as a PNG."""
    if isinstance(results, MonteCarloResult):
        values = [run.metrics["mean_remediation"] for run in results.runs]
    else:
        values = [metrics["mean_remediation"] for metrics in results]
    if not values:
        raise ValueError("results must contain at least one remediation value.")

    figure, axis = plt.subplots()
    axis.boxplot(values)
    axis.set_ylabel("Mean remediation fraction")
    figure.tight_layout()
    figure.savefig(filepath, format="png")
    plt.close(figure)
