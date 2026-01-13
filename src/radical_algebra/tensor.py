"""Tensor operations for radical algebra.

This module provides:
- TensorResult: Container for outer product results
- outer_product(): Compute outer product of a RadicalSet

Each tensor cell is a SET of valid characters, since multiple IDS
structures can map the same radical combination to different characters.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import product
from typing import TYPE_CHECKING

from radical_algebra.character_db import WU_XING_RADICALS, CharacterDatabase
from radical_algebra.exceptions import InvalidRankError
from radical_algebra.ids import build_ids_string, enumerate_structures


@lru_cache(maxsize=1)
def _get_cached_database() -> CharacterDatabase:
    """Get cached CharacterDatabase instance.

    Avoids rebuilding 88,937-entry database on every outer_product call.
    ~500x performance improvement for repeated calls.
    """
    return CharacterDatabase()


if TYPE_CHECKING:
    from radical_algebra.core import RadicalSet


class TensorResult:
    """Container for outer product results.

    Each cell contains a set of valid characters formed by combining
    the radicals at that index position.

    Attributes:
        shape: Tuple of dimensions (e.g., (5, 5) for rank-2 with 5 elements).
        rank: The tensor rank (2-5).
        radical_set: The original RadicalSet used.
    """

    def __init__(
        self,
        radical_set: RadicalSet,
        rank: int,
        data: dict[tuple[int, ...], set[str]],
    ) -> None:
        """Initialize a TensorResult.

        Args:
            radical_set: The RadicalSet used for this tensor.
            rank: The tensor rank.
            data: Dictionary mapping index tuples to character sets.
        """
        self._radical_set = radical_set
        self._rank = rank
        self._data = data
        self._size = len(radical_set)

    @property
    def shape(self) -> tuple[int, ...]:
        """Shape of the tensor (n repeated rank times)."""
        return (self._size,) * self._rank

    @property
    def rank(self) -> int:
        """The tensor rank (2-5)."""
        return self._rank

    @property
    def radical_set(self) -> RadicalSet:
        """The RadicalSet used for this tensor."""
        return self._radical_set

    def __getitem__(self, index: tuple[int, ...]) -> set[str]:
        """Get the character set at the given index.

        Args:
            index: Tuple of indices (e.g., (0, 0) for rank-2).

        Returns:
            Set of valid characters at this position.

        Raises:
            IndexError: If index is out of bounds.
        """
        if not isinstance(index, tuple):
            index = (index,)

        for i, idx in enumerate(index):
            if idx < 0 or idx >= self._size:
                raise IndexError(
                    f"Index {idx} out of bounds for dimension {i} with size {self._size}"
                )

        return self._data.get(index, set())


def outer_product(radical_set: RadicalSet, rank: int) -> TensorResult:
    """Compute the outer product of a RadicalSet.

    For rank-2: v ⊗ v^T yields an n×n matrix.
    For rank-3: v ⊗ v ⊗ v yields an n×n×n tensor.
    And so on for ranks 4-5.

    Each cell [i, j, ...] contains a SET of valid characters that can
    be formed by combining radical_set[i], radical_set[j], ... using
    various IDS structures.

    Args:
        radical_set: The RadicalSet to compute outer product of.
        rank: The tensor rank (2-5).

    Returns:
        TensorResult containing sets of valid characters.

    Raises:
        InvalidRankError: If rank is not between 2 and 5.
    """
    if rank < 2 or rank > 5:
        raise InvalidRankError(f"Rank must be between 2 and 5, got {rank}")

    db = _get_cached_database()
    n = len(radical_set)
    structures = enumerate_structures(rank)

    data: dict[tuple[int, ...], set[str]] = {}

    # Check if all radicals in the set are Wu Xing
    is_wu_xing_set = all(r in WU_XING_RADICALS for r in radical_set)

    # Generate all index combinations
    for indices in product(range(n), repeat=rank):
        radicals = [radical_set[i] for i in indices]

        if is_wu_xing_set:
            # For Wu Xing: composition-based lookup is most comprehensive
            # It recursively counts radicals and finds all matching characters
            radical_counts = dict(Counter(radicals))
            chars = db.lookup_by_composition(radical_counts)
        else:
            # For non-Wu Xing: use component-based lookup
            # Plus IDS structure enumeration for exact matches
            chars = set()
            for structure in structures:
                ids_string = build_ids_string(structure, radicals)
                chars.update(db.lookup_by_ids(ids_string))
            chars.update(db.lookup_by_components(radicals))

        data[indices] = chars

    return TensorResult(radical_set, rank, data)
