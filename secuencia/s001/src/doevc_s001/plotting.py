"""Visualization helpers for deterministic and Monte Carlo DoEVC outputs."""

from __future__ import annotations

from dataclasses import fields, replace
from os import PathLike
from pathlib import Path
from typing import Protocol, cast

import matplotlib

matplotlib.use("Agg")

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from .models import ModelParameters
from .montecarlo import MonteCarloRunResult
from .policies import Policy
from .simulation import simulate_deterministic_sprints
from .sprint import SprintState

type ParameterValue = int | float
type ParameterRange = tuple[str, tuple[ParameterValue, ...]]


class _Axes(Protocol):
    """Protocol covering the axes methods used by the plotting helpers."""

    def plot(
        self,
        x: tuple[int, ...],
        y: tuple[float, ...],
        *,
        label: str,
        linewidth: int,
    ) -> object: ...

    def set_xlabel(self, xlabel: str) -> object: ...

    def set_ylabel(self, ylabel: str) -> object: ...

    def set_title(self, title: str) -> object: ...

    def legend(self) -> object: ...

    def grid(self, visible: bool, *, alpha: float) -> None: ...

    def boxplot(self, x: tuple[float, ...]) -> object: ...

    def imshow(
        self,
        x: tuple[tuple[float, ...], ...],
        *,
        origin: str,
        aspect: str,
        vmin: float,
        vmax: float,
    ) -> object: ...

    def set_xticks(self, ticks: tuple[int, ...]) -> object: ...

    def set_yticks(self, ticks: tuple[int, ...]) -> object: ...

    def set_xticklabels(self, labels: tuple[str, ...]) -> object: ...

    def set_yticklabels(self, labels: tuple[str, ...]) -> object: ...


class _FigureSaver(Protocol):
    """Protocol covering the figure save method used by the plot helper."""

    def savefig(self, fname: str | PathLike[str], *, format: str) -> None: ...

    def colorbar(self, mappable: object, *, ax: _Axes) -> object: ...


def plot_simulation(
    states: tuple[SprintState, ...],
    destination: str | PathLike[str],
) -> Path:
    """Render backlog and technical debt trajectories as a PNG chart."""
    destination_path = Path(destination)
    sprint_indices = tuple(range(1, len(states) + 1))
    backlog_values = tuple(state.backlog for state in states)
    debt_values = tuple(state.technical_debt for state in states)

    figure = Figure(figsize=(8, 4.5), tight_layout=True)
    FigureCanvasAgg(figure)
    axes = cast(_Axes, figure.subplots())
    axes.plot(sprint_indices, backlog_values, label="B_k", linewidth=2)
    axes.plot(sprint_indices, debt_values, label="D_k", linewidth=2)
    axes.set_xlabel("Sprint")
    axes.set_ylabel("Trabajo pendiente")
    axes.set_title("Evolucion de backlog y deuda tecnica")
    axes.legend()
    axes.grid(True, alpha=0.3)
    cast(_FigureSaver, figure).savefig(destination_path, format="png")
    return destination_path


def plot_optimal_u_distribution(
    results: tuple[MonteCarloRunResult, ...],
    destination: str | PathLike[str],
) -> Path:
    """Render a PNG boxplot for the per-run optimal remediation distribution."""
    destination_path = Path(destination)
    remediation_values = tuple(run.average_remediation_fraction for run in results)
    if not remediation_values:
        raise ValueError("results must not be empty.")

    figure = Figure(figsize=(6, 4.5), tight_layout=True)
    FigureCanvasAgg(figure)
    axes = cast(_Axes, figure.subplots())
    axes.boxplot(remediation_values)
    axes.set_ylabel("u_k promedio")
    axes.set_title("Distribucion de u_k optimo")
    axes.grid(True, alpha=0.3)
    cast(_FigureSaver, figure).savefig(destination_path, format="png")
    return destination_path


def _average_remediation_fraction(trajectory: tuple[SprintState, ...]) -> float:
    """Return the mean remediation fraction, defaulting to zero for empty runs."""
    if not trajectory:
        return 0.0
    return sum(state.remediation_fraction for state in trajectory) / len(trajectory)


def _coerce_parameter_value(name: str, value: ParameterValue) -> ParameterValue:
    """Coerce one swept parameter value to the target ModelParameters field type."""
    if name == "K":
        if isinstance(value, int):
            return value
        if value.is_integer():
            return int(value)
        raise ValueError("K sweep values must be integers.")
    return float(value)


def _replace_parameter(
    parameters: ModelParameters,
    name: str,
    value: ParameterValue,
) -> ModelParameters:
    """Return a parameter set with one validated field replaced."""
    coerced = _coerce_parameter_value(name, value)
    if name == "B0":
        return replace(parameters, B0=float(coerced))
    if name == "D0":
        return replace(parameters, D0=float(coerced))
    if name == "V0":
        return replace(parameters, V0=float(coerced))
    if name == "alpha":
        return replace(parameters, alpha=float(coerced))
    if name == "beta":
        return replace(parameters, beta=float(coerced))
    if name == "gamma":
        return replace(parameters, gamma=float(coerced))
    if name == "theta":
        return replace(parameters, theta=float(coerced))
    if name == "lambda_":
        return replace(parameters, lambda_=float(coerced))
    if name == "rho":
        return replace(parameters, rho=float(coerced))
    if name == "K":
        return replace(parameters, K=int(coerced))
    if name == "s":
        return replace(parameters, s=float(coerced))
    raise ValueError("parameter name is not supported.")


def _validate_parameter_range(
    parameter_range: ParameterRange,
    *,
    label: str,
) -> ParameterRange:
    """Validate one named sweep range for the sensitivity heatmap."""
    parameter_name, values = parameter_range
    valid_names = {field.name for field in fields(ModelParameters)}
    if parameter_name not in valid_names:
        raise ValueError(f"{label} must name a ModelParameters field.")
    if not values:
        raise ValueError(f"{label} values must not be empty.")
    return parameter_range


def _build_sensitivity_matrix(
    param1_range: ParameterRange,
    param2_range: ParameterRange,
    base_parameters: ModelParameters,
    policy: Policy,
) -> tuple[tuple[float, ...], ...]:
    """Build the average-remediation matrix used by the sensitivity heatmap."""
    param1_name, param1_values = _validate_parameter_range(
        param1_range,
        label="param1_range",
    )
    param2_name, param2_values = _validate_parameter_range(
        param2_range,
        label="param2_range",
    )
    if param1_name == param2_name:
        raise ValueError("param1_range and param2_range must target distinct fields.")

    matrix_rows: list[tuple[float, ...]] = []
    for param2_value in param2_values:
        row: list[float] = []
        for param1_value in param1_values:
            parameters = _replace_parameter(base_parameters, param1_name, param1_value)
            parameters = _replace_parameter(parameters, param2_name, param2_value)
            trajectory = simulate_deterministic_sprints(parameters, policy)
            row.append(_average_remediation_fraction(trajectory))
        matrix_rows.append(tuple(row))
    return tuple(matrix_rows)


def plot_sensitivity_heatmap(
    param1_range: ParameterRange,
    param2_range: ParameterRange,
    base_parameters: ModelParameters,
    policy: Policy,
    destination: str | PathLike[str],
) -> Path:
    """Render a PNG heatmap of average remediation across two parameter sweeps."""
    destination_path = Path(destination)
    param1_name, param1_values = _validate_parameter_range(
        param1_range,
        label="param1_range",
    )
    param2_name, param2_values = _validate_parameter_range(
        param2_range,
        label="param2_range",
    )
    matrix = _build_sensitivity_matrix(
        param1_range,
        param2_range,
        base_parameters,
        policy,
    )

    figure = Figure(figsize=(7, 5), tight_layout=True)
    FigureCanvasAgg(figure)
    axes = cast(_Axes, figure.subplots())
    image = axes.imshow(matrix, origin="lower", aspect="auto", vmin=0.0, vmax=1.0)
    axes.set_xlabel(param1_name)
    axes.set_ylabel(param2_name)
    axes.set_title("Mapa de sensibilidad de u_k promedio")
    axes.set_xticks(tuple(range(len(param1_values))))
    axes.set_yticks(tuple(range(len(param2_values))))
    axes.set_xticklabels(tuple(f"{value:g}" for value in param1_values))
    axes.set_yticklabels(tuple(f"{value:g}" for value in param2_values))
    cast(_FigureSaver, figure).colorbar(image, ax=axes)
    cast(_FigureSaver, figure).savefig(destination_path, format="png")
    return destination_path
