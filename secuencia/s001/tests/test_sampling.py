"""Tests for reproducible random model parameter sampling."""

from doevc_s001 import ModelParameters, sample_model_parameters


def base_parameters() -> ModelParameters:
    """Return the deterministic parameters retained by the sampler."""
    return ModelParameters(
        B0=100.0,
        D0=20.0,
        V0=12.0,
        alpha=0.3,
        beta=0.1,
        gamma=0.05,
        theta=0.2,
        lambda_=0.8,
        rho=0.4,
        K=16,
        s=1.0,
    )


def test_sampling_with_same_seed_is_reproducible() -> None:
    """Return the same complete parameter set for an identical seed."""
    parameters = base_parameters()

    assert sample_model_parameters(
        parameters,
        seed=1234,
    ) == sample_model_parameters(parameters, seed=1234)


def test_sampling_uses_the_reference_uniform_ranges() -> None:
    """Sample every uncertain parameter inside its specified reference range."""
    sampled = sample_model_parameters(base_parameters(), seed=42)

    assert 1.0 <= sampled.s <= 1.4
    assert 0.0 <= sampled.gamma <= 0.05
    assert 0.0 <= sampled.theta <= 0.9
    assert 0.5 <= 1.0 - sampled.beta <= 0.9
    assert 0.2 <= sampled.lambda_ <= 1.0


def test_sampling_returns_complete_parameters_with_fixed_values_preserved() -> None:
    """Keep deterministic model values when sampling the uncertain values."""
    parameters = base_parameters()
    sampled = sample_model_parameters(parameters, seed=7)

    assert sampled.B0 == parameters.B0
    assert sampled.D0 == parameters.D0
    assert sampled.V0 == parameters.V0
    assert sampled.alpha == parameters.alpha
    assert sampled.rho == parameters.rho
    assert sampled.K == parameters.K
