"""Shared test data builders."""

from s004 import ModelParameters
from s004.monte_carlo import DEFAULT_MODEL_PARAMETERS


def create_parameters() -> ModelParameters:
    """Return a representative valid parameter set."""
    return DEFAULT_MODEL_PARAMETERS
