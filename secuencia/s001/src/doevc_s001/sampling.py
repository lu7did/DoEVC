"""Uniform random sampling helpers for the DoEVC s001 sequence."""

from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import ClassVar

from .models import ModelParameters

type RandomSeed = int | float | str | bytes | bytearray | None


@dataclass(slots=True)
class UniformParameterSampler:
    """Sample reproducible model parameters using the story C1 uniform ranges."""

    base_parameters: ModelParameters
    seed: RandomSeed = None
    _generator: Random = field(init=False, repr=False)

    S_RANGE: ClassVar[tuple[float, float]] = (1.0, 1.4)
    GAMMA_RANGE: ClassVar[tuple[float, float]] = (0.0, 0.05)
    THETA_RANGE: ClassVar[tuple[float, float]] = (0.0, 0.9)
    ONE_MINUS_BETA_RANGE: ClassVar[tuple[float, float]] = (0.5, 0.9)
    LAMBDA_RANGE: ClassVar[tuple[float, float]] = (0.2, 1.0)

    def __post_init__(self) -> None:
        """Initialize the deterministic random generator."""
        self._generator = Random(self.seed)  # nosec B311 - reproducible sampling

    def reseed(self, seed: RandomSeed) -> None:
        """Reset the generator state to reproduce the same sampling sequence."""
        self.seed = seed
        self._generator = Random(seed)  # nosec B311 - reproducible sampling

    def sample(self) -> ModelParameters:
        """Return a complete parameter set with the C1 fields sampled uniformly."""
        sampled_s = self._generator.uniform(*self.S_RANGE)
        sampled_gamma = self._generator.uniform(*self.GAMMA_RANGE)
        sampled_theta = self._generator.uniform(*self.THETA_RANGE)
        one_minus_beta = self._generator.uniform(*self.ONE_MINUS_BETA_RANGE)
        sampled_lambda = self._generator.uniform(*self.LAMBDA_RANGE)
        return ModelParameters(
            B0=self.base_parameters.B0,
            D0=self.base_parameters.D0,
            V0=self.base_parameters.V0,
            alpha=self.base_parameters.alpha,
            beta=1.0 - one_minus_beta,
            gamma=sampled_gamma,
            theta=sampled_theta,
            lambda_=sampled_lambda,
            rho=self.base_parameters.rho,
            K=self.base_parameters.K,
            s=sampled_s,
        )


def sample_uniform_parameters(
    base_parameters: ModelParameters,
    seed: RandomSeed = None,
) -> ModelParameters:
    """Sample one reproducible parameter set using the story C1 uniform ranges."""
    return UniformParameterSampler(base_parameters=base_parameters, seed=seed).sample()
