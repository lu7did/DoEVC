"""Regression tests for uncertain parameter sampling."""

from doevc_s002 import ModelParameters, sample_model_parameters


def _base_parameters() -> ModelParameters:
    """Create deterministic model values retained by the sampler."""
    return ModelParameters(100, 20, 10, 0.1, 0.2, 0.01, 0.3, 0.5, 0.4, 12)


def test_sampling_is_reproducible_for_a_fixed_seed() -> None:
    """Return exactly the same complete parameter set for equal seeds."""
    assert sample_model_parameters(_base_parameters(), 42) == sample_model_parameters(
        _base_parameters(), 42
    )


def test_sampling_stays_inside_documented_uniform_ranges() -> None:
    """Sample each uncertain field inside its reference interval."""
    parameters = sample_model_parameters(_base_parameters(), 7)

    assert 1.0 <= parameters.s <= 1.4
    assert 0.0 <= parameters.gamma <= 0.05
    assert 0.0 <= parameters.theta <= 0.9
    assert 0.5 <= 1 - parameters.beta <= 0.9
    assert 0.2 <= parameters.lambda_ <= 1.0
