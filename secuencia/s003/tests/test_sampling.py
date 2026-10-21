"""Regression tests for reproducible parameter sampling in s003."""

from doevc_s003 import ModelParameters, sample_model_parameters


def _template() -> ModelParameters:
    """Create the stable fields used by sampling scenarios."""
    return ModelParameters(100, 20, 10, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 7)


def test_sampling_is_reproducible_with_the_same_seed() -> None:
    """Produce the same full parameter set for an identical seed."""
    assert sample_model_parameters(_template(), seed=2026) == sample_model_parameters(
        _template(), seed=2026
    )


def test_sampling_respects_reference_uniform_ranges() -> None:
    """Keep sampled fields inside their respective stated intervals."""
    template = _template()
    sampled = sample_model_parameters(template, seed=7)

    assert 1.0 <= sampled.V0 / template.V0 <= 1.4
    assert 0.0 <= sampled.gamma <= 0.05
    assert 0.0 <= sampled.theta <= 0.9
    assert 0.5 <= 1 - sampled.beta <= 0.9
    assert 0.2 <= sampled.lambda_ <= 1.0


def test_sampling_preserves_unsampled_template_fields() -> None:
    """Retain complete model inputs outside the uncertainty ranges."""
    template = _template()
    sampled = sample_model_parameters(template, seed=1)

    assert (sampled.B0, sampled.D0, sampled.alpha, sampled.rho, sampled.K) == (
        template.B0,
        template.D0,
        template.alpha,
        template.rho,
        template.K,
    )
