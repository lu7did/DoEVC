"""Reproducible uniform sampling of model parameters."""

from random import Random

from .models import ModelParameters


def sample_model_parameters(
    template: ModelParameters, seed: int | None = None
) -> ModelParameters:
    """Sample a complete parameter set from the reference uniform ranges."""
    generator = Random(seed)
    velocity_scale = generator.uniform(1.0, 1.4)
    gamma = generator.uniform(0.0, 0.05)
    theta = generator.uniform(0.0, 0.9)
    beta = 1 - generator.uniform(0.5, 0.9)
    lambda_ = generator.uniform(0.2, 1.0)
    return ModelParameters(
        B0=template.B0,
        D0=template.D0,
        V0=template.V0 * velocity_scale,
        alpha=template.alpha,
        beta=beta,
        gamma=gamma,
        theta=theta,
        lambda_=lambda_,
        rho=template.rho,
        K=template.K,
    )
