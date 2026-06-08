"""Tests for deterministic, Monte Carlo, and sensitivity plotting helpers."""

import pytest

from doevc_s001 import (
    DebtFirstPolicy,
    EconomicObjectiveFunction,
    FixedRemediationPolicy,
    ModelParameters,
    OptimalLocalPolicy,
    plot_optimal_u_distribution,
    plot_sensitivity_heatmap,
    plot_simulation,
    run_monte_carlo,
    simulate_deterministic_sprints,
)
from doevc_s001.plotting import (
    _average_remediation_fraction,
    _build_sensitivity_matrix,
    _replace_parameter,
)


def sample_parameters() -> ModelParameters:
    """Return a representative parameter set for plotting tests."""
    return ModelParameters(
        B0=8.0,
        D0=4.0,
        V0=4.0,
        alpha=0.0,
        beta=0.2,
        gamma=0.01,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=3,
        s=1.0,
    )


def test_plot_simulation_creates_a_non_empty_png(tmp_path: str) -> None:
    """Create a PNG file for a deterministic sprint trajectory."""
    states = simulate_deterministic_sprints(sample_parameters(), DebtFirstPolicy())

    png_path = plot_simulation(states, tmp_path / "simulation.png")

    assert png_path.exists()
    assert png_path.suffix == ".png"
    assert png_path.stat().st_size > 0
    assert png_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_plot_optimal_u_distribution_creates_a_non_empty_png(tmp_path: str) -> None:
    """Create a PNG boxplot from valid Monte Carlo run results."""
    result = run_monte_carlo(
        4,
        OptimalLocalPolicy(objective=EconomicObjectiveFunction()),
        seed=321,
        base_parameters=sample_parameters(),
    )

    png_path = plot_optimal_u_distribution(
        result.runs,
        tmp_path / "optimal-u-distribution.png",
    )

    assert png_path.exists()
    assert png_path.suffix == ".png"
    assert png_path.stat().st_size > 0
    assert png_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_plot_optimal_u_distribution_rejects_empty_results(tmp_path: str) -> None:
    """Reject boxplot generation without any Monte Carlo runs."""
    with pytest.raises(ValueError, match="results must not be empty"):
        plot_optimal_u_distribution((), tmp_path / "empty-optimal-u.png")


def test_average_remediation_fraction_returns_zero_for_empty_trajectory() -> None:
    """Treat empty deterministic trajectories as zero average remediation."""
    assert _average_remediation_fraction(()) == 0.0


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("B0", 7.5),
        ("D0", 3.5),
        ("V0", 5.5),
        ("alpha", 0.1),
        ("beta", 0.3),
        ("lambda_", 0.9),
        ("rho", 0.6),
        ("s", 1.2),
    ],
)
def test_replace_parameter_updates_supported_fields(
    field_name: str,
    value: float,
) -> None:
    """Replace each supported float field without affecting the others."""
    updated = _replace_parameter(sample_parameters(), field_name, value)

    assert getattr(updated, field_name) == value


def test_replace_parameter_rejects_unknown_names() -> None:
    """Reject replacement requests for unsupported parameter names."""
    with pytest.raises(ValueError, match="parameter name is not supported"):
        _replace_parameter(sample_parameters(), "unknown", 1.0)


def test_build_sensitivity_matrix_returns_expected_dimensions() -> None:
    """Build a matrix with expected row and column counts."""
    matrix = _build_sensitivity_matrix(
        ("gamma", (0.0, 0.02, 0.04)),
        ("theta", (0.1, 0.3)),
        sample_parameters(),
        FixedRemediationPolicy(0.25),
    )

    assert len(matrix) == 2
    assert all(len(row) == 3 for row in matrix)
    assert matrix == ((0.25, 0.25, 0.25), (0.25, 0.25, 0.25))


def test_build_sensitivity_matrix_rejects_duplicate_parameter_names() -> None:
    """Reject sensitivity matrices that try to sweep the same field twice."""
    with pytest.raises(ValueError, match="must target distinct fields"):
        _build_sensitivity_matrix(
            ("gamma", (0.0, 0.02)),
            ("gamma", (0.1, 0.3)),
            sample_parameters(),
            FixedRemediationPolicy(0.25),
        )


def test_plot_sensitivity_heatmap_creates_a_non_empty_png(tmp_path: str) -> None:
    """Create a PNG heatmap for a named two-parameter sensitivity sweep."""
    png_path = plot_sensitivity_heatmap(
        ("gamma", (0.0, 0.02, 0.04)),
        ("theta", (0.1, 0.3)),
        sample_parameters(),
        FixedRemediationPolicy(0.25),
        tmp_path / "sensitivity-heatmap.png",
    )

    assert png_path.exists()
    assert png_path.suffix == ".png"
    assert png_path.stat().st_size > 0
    assert png_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_plot_sensitivity_heatmap_accepts_zero_work_parameter_sweeps(
    tmp_path: str,
) -> None:
    """Allow empty trajectories by rendering zero average remediation cells."""
    png_path = plot_sensitivity_heatmap(
        ("B0", (0.0, 1.0)),
        ("D0", (0.0, 2.0)),
        sample_parameters(),
        FixedRemediationPolicy(0.25),
        tmp_path / "zero-work-heatmap.png",
    )

    assert png_path.exists()
    assert png_path.stat().st_size > 0


def test_plot_sensitivity_heatmap_rejects_unknown_parameter_names(
    tmp_path: str,
) -> None:
    """Reject sweeps that do not target valid ModelParameters fields."""
    with pytest.raises(ValueError, match="must name a ModelParameters field"):
        plot_sensitivity_heatmap(
            ("unknown", (0.1, 0.2)),
            ("theta", (0.1, 0.3)),
            sample_parameters(),
            FixedRemediationPolicy(0.25),
            tmp_path / "invalid-heatmap.png",
        )


def test_plot_sensitivity_heatmap_rejects_empty_parameter_values(
    tmp_path: str,
) -> None:
    """Reject sweeps that do not provide any values."""
    with pytest.raises(ValueError, match="values must not be empty"):
        plot_sensitivity_heatmap(
            ("gamma", ()),
            ("theta", (0.1, 0.3)),
            sample_parameters(),
            FixedRemediationPolicy(0.25),
            tmp_path / "empty-heatmap.png",
        )


def test_plot_sensitivity_heatmap_accepts_integer_valued_k_sweeps(
    tmp_path: str,
) -> None:
    """Allow sweeping K when the provided values are integer-valued."""
    png_path = plot_sensitivity_heatmap(
        ("K", (2, 3, 4.0)),
        ("gamma", (0.0, 0.02)),
        sample_parameters(),
        FixedRemediationPolicy(0.25),
        tmp_path / "k-heatmap.png",
    )

    assert png_path.exists()
    assert png_path.stat().st_size > 0


def test_plot_sensitivity_heatmap_rejects_non_integer_k_sweeps(tmp_path: str) -> None:
    """Reject K sweeps that contain non-integer values."""
    with pytest.raises(ValueError, match="K sweep values must be integers"):
        plot_sensitivity_heatmap(
            ("K", (2.5,)),
            ("gamma", (0.0, 0.02)),
            sample_parameters(),
            FixedRemediationPolicy(0.25),
            tmp_path / "invalid-k-heatmap.png",
        )
