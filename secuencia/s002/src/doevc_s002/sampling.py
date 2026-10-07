"""Reproducible sampling of uncertain model parameters."""

from dataclasses import replace
from random import Random

from .models import ModelParameters


def sample_model_parameters(
    base_parameters: ModelParameters, seed: int | None = None
) -> ModelParameters:
    """Sample the documented uniform uncertainty ranges from a base model."""
    random = Random(seed)
    return replace(
        base_parameters,
        s=random.uniform(1.0, 1.4),
        gamma=random.uniform(0.0, 0.05),
        theta=random.uniform(0.0, 0.9),
        beta=1 - random.uniform(0.5, 0.9),
        lambda_=random.uniform(0.2, 1.0),
    )
