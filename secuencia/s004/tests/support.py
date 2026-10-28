"""Shared test data builders."""

from s004 import ModelParameters
from s004.monte_carlo import DEFAULT_MODEL_PARAMETERS


def create_parameters() -> ModelParameters:
    """Return a representative valid parameter set."""
    return DEFAULT_MODEL_PARAMETERS


def create_competing_parameters() -> ModelParameters:
    """Return a one-sprint scenario where backlog and debt compete."""
    return ModelParameters(
        B0=10.0,
        D0=10.0,
        V0=10.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.0,
        lambda_=0.0,
        rho=0.0,
        K=1,
    )


def create_backlog_only_parameters() -> ModelParameters:
    """Return a one-sprint model with known fixed-fraction outcomes."""
    return ModelParameters(
        B0=10.0,
        D0=0.0,
        V0=10.0,
        alpha=0.0,
        beta=0.0,
        gamma=0.0,
        theta=0.0,
        lambda_=0.0,
        rho=0.0,
        K=1,
    )
