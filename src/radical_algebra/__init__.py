"""Tensor algebra on Chinese radicals.

Find valid CJKV character combinations (excluding simplified Chinese)
via outer products and higher-rank tensor operations.
"""

from radical_algebra.core import RadicalSet
from radical_algebra.exceptions import (
    InvalidRadicalError,
    InvalidRankError,
    RadicalAlgebraError,
    SimplifiedChineseError,
)
from radical_algebra.presets import WU_XING
from radical_algebra.tensor import TensorResult, outer_product

__version__ = "0.1.0"

__all__ = [
    # Core classes
    "RadicalSet",
    "TensorResult",
    # Functions
    "outer_product",
    # Exceptions
    "RadicalAlgebraError",
    "InvalidRadicalError",
    "SimplifiedChineseError",
    "InvalidRankError",
    # Presets
    "WU_XING",
    # Version
    "__version__",
]
