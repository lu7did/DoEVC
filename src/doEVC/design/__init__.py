"""
doEVC.design – Experimental design generation utilities.

Provides helpers to build common experimental designs used in the
Voltage Control (VC) study:

- Full factorial designs
- Fractional factorial designs
- Central Composite Designs (CCD) for Response Surface Methodology (RSM)
- Latin Hypercube Sampling (LHS)
"""

from doEVC.design.factorial import full_factorial, fractional_factorial
from doEVC.design.response_surface import central_composite
from doEVC.design.lhs import latin_hypercube

__all__ = [
    "full_factorial",
    "fractional_factorial",
    "central_composite",
    "latin_hypercube",
]
