"""Non-interactive visualizations for deterministic simulations."""

# pyright: reportUnknownMemberType=false

from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path
from statistics import fmean

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from .models import ModelParameters
from .monte_carlo import MonteCarloResult, MonteCarloSimulation
from .policies import Policy
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

_VARIABLE_PARAMETER_NAMES = frozenset(
    {"B0", "D0", "V0", "alpha", "beta", "gamma", "theta", "lambda_", "rho", "s"}
)


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


def plot_sensitivity_heatmap(
    param1_range: tuple[str, Sequence[float]],
    param2_range: tuple[str, Sequence[float]],
    base_params: ModelParameters,
    policy: Policy,
    filepath: str | Path,
) -> tuple[tuple[float, ...], ...]:
    """Render mean remediation fractions across two parameter ranges."""
    param1_name, param1_values = _validate_parameter_range(param1_range)
    param2_name, param2_values = _validate_parameter_range(param2_range)
    matrix = tuple(
        tuple(
            _mean_remediation_fraction(
                _replace_parameter(
                    _replace_parameter(base_params, param1_name, param1_value),
                    param2_name,
                    param2_value,
                ),
                policy,
            )
            for param1_value in param1_values
        )
        for param2_value in param2_values
    )

    figure, axis = plt.subplots()
    image = axis.imshow(matrix, aspect="auto", origin="lower")
    axis.set_xlabel(param1_name)
    axis.set_ylabel(param2_name)
    axis.set_xticks(range(len(param1_values)), tuple(map(str, param1_values)))
    axis.set_yticks(range(len(param2_values)), tuple(map(str, param2_values)))
    figure.colorbar(image, ax=axis, label="Mean u_k")
    figure.tight_layout()
    figure.savefig(filepath, format="png")
    plt.close(figure)
    return matrix


def _validate_parameter_range(
    parameter_range: tuple[str, Sequence[float]],
) -> tuple[str, Sequence[float]]:
    """Validate a named non-empty range for a model parameter."""
    name, values = parameter_range
    if name not in _VARIABLE_PARAMETER_NAMES:
        raise ValueError(f"unknown model parameter: {name}.")
    if not values:
        raise ValueError(f"parameter range for {name} must not be empty.")
    return name, values


def _replace_parameter(
    parameters: ModelParameters,
    name: str,
    value: float,
) -> ModelParameters:
    """Replace one continuous model parameter selected for sensitivity analysis."""
    match name:
        case "B0":
            return replace(parameters, B0=value)
        case "D0":
            return replace(parameters, D0=value)
        case "V0":
            return replace(parameters, V0=value)
        case "alpha":
            return replace(parameters, alpha=value)
        case "beta":
            return replace(parameters, beta=value)
        case "gamma":
            return replace(parameters, gamma=value)
        case "theta":
            return replace(parameters, theta=value)
        case "lambda_":
            return replace(parameters, lambda_=value)
        case "rho":
            return replace(parameters, rho=value)
        case "s":
            return replace(parameters, s=value)
        case _:
            raise ValueError(f"unknown model parameter: {name}.")


def _mean_remediation_fraction(
    parameters: ModelParameters,
    policy: Policy,
) -> float:
    """Calculate the mean remediation fraction for one parameter combination."""
    states = simulate_deterministic_sprints(parameters, policy)
    if not states:
        return 0.0
    return fmean(state.remediation_fraction for state in states)
