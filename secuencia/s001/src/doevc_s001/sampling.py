"""Reproducible sampling of uncertain model parameters."""

from random import Random

from .models import ModelParameters


def sample_model_parameters(
    base_parameters: ModelParameters,
    *,
    seed: int | None = None,
) -> ModelParameters:
    """Sample uncertain parameters from their reference uniform distributions."""
    # This pseudo-random generator provides reproducible scientific samples.
    generator = Random(seed)  # nosec B311
    return ModelParameters(
        B0=base_parameters.B0,
        D0=base_parameters.D0,
        V0=base_parameters.V0,
        alpha=base_parameters.alpha,
        beta=1.0 - generator.uniform(0.5, 0.9),
        gamma=generator.uniform(0.0, 0.05),
        theta=generator.uniform(0.0, 0.9),
        lambda_=generator.uniform(0.2, 1.0),
        rho=base_parameters.rho,
        K=base_parameters.K,
        s=generator.uniform(1.0, 1.4),
    )
