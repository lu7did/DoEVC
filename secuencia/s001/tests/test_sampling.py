"""Tests for story C1 uniform parameter sampling in DoEVC s001."""

import math

from doevc_s001 import (
    ModelParameters,
    UniformParameterSampler,
    sample_uniform_parameters,
)


def base_parameters() -> ModelParameters:
    """Return the deterministic fields kept fixed during C1 sampling."""
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


def test_sample_uniform_parameters_returns_complete_model_parameters() -> None:
    """Return a complete parameter object while preserving fixed inputs."""
    sampled = sample_uniform_parameters(base_parameters(), seed=7)

    assert isinstance(sampled, ModelParameters)
    assert sampled.B0 == 100.0
    assert sampled.D0 == 20.0
    assert sampled.V0 == 12.0
    assert sampled.alpha == 0.3
    assert sampled.rho == 0.4
    assert sampled.K == 16


def test_uniform_parameter_sampler_reproduces_first_sample_with_same_seed() -> None:
    """Produce the same first draw when the seed and base values are the same."""
    first_sampler = UniformParameterSampler(
        base_parameters=base_parameters(),
        seed=12345,
    )
    second_sampler = UniformParameterSampler(
        base_parameters=base_parameters(),
        seed=12345,
    )

    assert first_sampler.sample() == second_sampler.sample()


def test_uniform_parameter_sampler_reseed_restarts_sampling_sequence() -> None:
    """Allow replaying the same sample sequence after reseeding."""
    sampler = UniformParameterSampler(base_parameters=base_parameters(), seed=99)

    first_sample = sampler.sample()
    sampler.reseed(99)

    assert sampler.sample() == first_sample


def test_sample_uniform_parameters_respects_story_c1_reference_ranges() -> None:
    """Keep the random values inside the documented uniform intervals."""
    sampled = sample_uniform_parameters(base_parameters(), seed=2026)

    assert 1.0 <= sampled.s <= 1.4
    assert 0.0 <= sampled.gamma <= 0.05
    assert 0.0 <= sampled.theta <= 0.9
    assert 0.5 <= 1.0 - sampled.beta <= 0.9
    assert 0.2 <= sampled.lambda_ <= 1.0


def test_sample_uniform_parameters_fixed_seed_regression() -> None:
    """Keep the fixed-seed sample stable for reproducibility checks."""
    sampled = sample_uniform_parameters(base_parameters(), seed=20260602)

    assert math.isclose(sampled.s, 1.1305955555109137)
    assert math.isclose(sampled.gamma, 0.02064374969727912)
    assert math.isclose(sampled.theta, 0.4063854046982147)
    assert math.isclose(sampled.beta, 0.15208741265631254)
    assert math.isclose(sampled.lambda_, 0.739659056745726)
