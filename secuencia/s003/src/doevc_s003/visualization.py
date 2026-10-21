"""Non-interactive visualizations for deterministic simulations."""

# pyright: reportUnknownMemberType=false
# pylint: disable=wrong-import-position

from collections.abc import Sequence
from dataclasses import dataclass
from numbers import Real
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot as plt

from .models import ModelParameters
from .monte_carlo import MonteCarloResult, RunMetrics
from .policies import Policy
from .simulation import simulate_sprints
from .sprint import SprintState

ParameterRange = tuple[str, Sequence[float]]
_VARIABLE_PARAMETERS = frozenset(
    {"B0", "D0", "V0", "alpha", "beta", "gamma", "theta", "lambda_", "rho"}
)


@dataclass(frozen=True, slots=True)
class _SensitivityAxes:
    """Names and values used to construct a sensitivity matrix."""

    param1_name: str
    param1_values: tuple[float, ...]
    param2_name: str
    param2_values: tuple[float, ...]


def _prepare_parameter_range(
    parameter_range: ParameterRange, range_name: str
) -> tuple[str, tuple[float, ...]]:
    """Validate a named non-empty sequence of model parameter values."""
    parameter_name, values = parameter_range
    if parameter_name not in _VARIABLE_PARAMETERS:
        raise ValueError(f"{range_name} names an unsupported model parameter.")
    if any(isinstance(value, bool) or not isinstance(value, Real) for value in values):
        raise TypeError(f"{range_name} values must be real numbers.")
    numeric_values = tuple(float(value) for value in values)
    if not numeric_values:
        raise ValueError(f"{range_name} must contain at least one value.")
    return parameter_name, numeric_values


def _replace_variable_parameter(
    parameters: ModelParameters, parameter_name: str, value: float
) -> ModelParameters:
    """Return parameters with one supported sensitivity field replaced."""
    if parameter_name not in _VARIABLE_PARAMETERS:
        raise ValueError(f"unsupported model parameter: {parameter_name}.")
    parameter_values = parameters.to_dict()
    parameter_values[parameter_name] = value
    return ModelParameters(
        B0=float(parameter_values["B0"]),
        D0=float(parameter_values["D0"]),
        V0=float(parameter_values["V0"]),
        alpha=float(parameter_values["alpha"]),
        beta=float(parameter_values["beta"]),
        gamma=float(parameter_values["gamma"]),
        theta=float(parameter_values["theta"]),
        lambda_=float(parameter_values["lambda_"]),
        rho=float(parameter_values["rho"]),
        K=int(parameter_values["K"]),
    )


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


def _average_allocation(
    base_params: ModelParameters,
    policy: Policy,
    axes: _SensitivityAxes,
    param1_value: float,
    param2_value: float,
) -> float:
    """Run one sensitivity scenario and return its average allocation."""
    parameters = _replace_variable_parameter(
        _replace_variable_parameter(base_params, axes.param1_name, param1_value),
        axes.param2_name,
        param2_value,
    )
    trajectory = simulate_sprints(parameters, policy)
    return (
        sum(state.allocation for state in trajectory) / len(trajectory)
        if trajectory
        else 0.0
    )


def _save_heatmap(
    matrix: list[list[float]],
    axes: _SensitivityAxes,
    filepath: str | Path,
) -> None:
    """Render the sensitivity matrix as a PNG heatmap."""
    figure, plot_axes = plt.subplots()
    image = plot_axes.imshow(matrix, aspect="auto", origin="lower")
    plot_axes.set_xlabel(axes.param1_name)
    plot_axes.set_ylabel(axes.param2_name)
    plot_axes.set_xticks(
        range(len(axes.param1_values)), [str(value) for value in axes.param1_values]
    )
    plot_axes.set_yticks(
        range(len(axes.param2_values)), [str(value) for value in axes.param2_values]
    )
    plot_axes.set_title("Average remediation allocation sensitivity")
    figure.colorbar(image, ax=plot_axes, label="Average u_k")
    figure.tight_layout()
    figure.savefig(Path(filepath), format="png")
    plt.close(figure)


def plot_sensitivity_heatmap(
    param1_range: ParameterRange,
    param2_range: ParameterRange,
    base_params: ModelParameters,
    policy: Policy,
    filepath: str | Path,
) -> list[list[float]]:
    """Plot average allocations across a two-parameter sensitivity grid."""
    param1_name, param1_values = _prepare_parameter_range(param1_range, "param1_range")
    param2_name, param2_values = _prepare_parameter_range(param2_range, "param2_range")
    if param1_name == param2_name:
        raise ValueError("sensitivity ranges must name different parameters.")
    axes = _SensitivityAxes(
        param1_name,
        param1_values,
        param2_name,
        param2_values,
    )

    matrix: list[list[float]] = []
    for param2_value in axes.param2_values:
        row: list[float] = []
        for param1_value in axes.param1_values:
            row.append(
                _average_allocation(
                    base_params,
                    policy,
                    axes,
                    param1_value,
                    param2_value,
                )
            )
        matrix.append(row)

    _save_heatmap(
        matrix,
        axes,
        filepath,
    )
    return matrix
