"""Tests for reproducible model parameter sampling."""

from s004 import sample_model_parameters
from tests.support import create_parameters


def test_sampling_with_same_seed_is_reproducible() -> None:
    """An identical seed produces the same complete parameter set."""
    parameters = create_parameters()

    assert sample_model_parameters(
        parameters,
        seed=1234,
    ) == sample_model_parameters(parameters, seed=1234)


def test_sampling_uses_reference_uniform_ranges() -> None:
    """Sample each uncertain parameter inside its documented range."""
    sampled = sample_model_parameters(create_parameters(), seed=42)

    assert 1.0 <= sampled.s <= 1.4
    assert 0.0 <= sampled.gamma <= 0.05
    assert 0.0 <= sampled.theta <= 0.9
    assert 0.5 <= 1.0 - sampled.beta <= 0.9
    assert 0.2 <= sampled.lambda_ <= 1.0


def test_sampling_preserves_deterministic_parameters() -> None:
    """Only uncertain parameters vary during sampling."""
    parameters = create_parameters()
    sampled = sample_model_parameters(parameters, seed=7)

    assert sampled.B0 == parameters.B0
    assert sampled.D0 == parameters.D0
    assert sampled.V0 == parameters.V0
    assert sampled.alpha == parameters.alpha
    assert sampled.rho == parameters.rho
    assert sampled.K == parameters.K
