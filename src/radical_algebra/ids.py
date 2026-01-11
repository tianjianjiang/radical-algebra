"""IDS (Ideographic Description Sequence) operators and structure enumeration.

This module provides:
- IDS operator constants (binary: 10, ternary: 2)
- IDSStructure dataclass for representing composition trees
- DP-based enumeration of all possible IDS structures for n components
- Building IDS strings from structures and radicals
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class IDSOperator:
    """An IDS operator with its Unicode symbol and arity.

    Attributes:
        symbol: The Unicode IDS operator character.
        arity: Number of components this operator takes (2 or 3).
        name: Human-readable name for this operator.
    """

    symbol: str
    arity: int
    name: str


BINARY_OPS: tuple[IDSOperator, ...] = (
    IDSOperator("⿰", 2, "LEFT_RIGHT"),
    IDSOperator("⿱", 2, "TOP_BOTTOM"),
    IDSOperator("⿴", 2, "SURROUND_FULL"),
    IDSOperator("⿵", 2, "SURROUND_ABOVE"),
    IDSOperator("⿶", 2, "SURROUND_BELOW"),
    IDSOperator("⿷", 2, "SURROUND_LEFT"),
    IDSOperator("⿸", 2, "SURROUND_UPPER_LEFT"),
    IDSOperator("⿹", 2, "SURROUND_UPPER_RIGHT"),
    IDSOperator("⿺", 2, "SURROUND_LOWER_LEFT"),
    IDSOperator("⿻", 2, "OVERLAID"),
)

TERNARY_OPS: tuple[IDSOperator, ...] = (
    IDSOperator("⿲", 3, "LEFT_MID_RIGHT"),
    IDSOperator("⿳", 3, "TOP_MID_BOTTOM"),
)


@dataclass(frozen=True)
class IDSStructure:
    """A tree structure representing how components are composed.

    Leaf nodes have no operator and represent a single component.
    Internal nodes have an operator and children.

    Attributes:
        operator: The IDS operator at this node (None for leaf).
        children: Child structures (empty for leaf).
    """

    operator: IDSOperator | None = None
    children: tuple[IDSStructure, ...] = ()

    @property
    def is_leaf(self) -> bool:
        """True if this is a leaf node (single component)."""
        return self.operator is None

    @property
    def component_count(self) -> int:
        """Total number of leaf components in this structure."""
        if self.is_leaf:
            return 1
        return sum(child.component_count for child in self.children)

    @property
    def depth(self) -> int:
        """Depth of the tree (0 for leaf, 1+ for internal nodes)."""
        if self.is_leaf:
            return 0
        return 1 + max(child.depth for child in self.children)


LEAF = IDSStructure()


@lru_cache(maxsize=16)
def enumerate_structures(n: int) -> tuple[IDSStructure, ...]:
    """Enumerate all possible IDS tree structures for n components.

    Uses dynamic programming: T(n) depends on T(k) for k < n.

    T(1) = 1 (leaf)
    T(2) = 10 (binary operators on 2 leaves)
    T(3) = 10 × (T(1)×T(2) + T(2)×T(1)) + 2 = 202

    Args:
        n: Number of components (must be >= 1).

    Returns:
        Tuple of all possible IDSStructure objects.

    Raises:
        ValueError: If n < 1.
    """
    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}")

    if n == 1:
        return (LEAF,)

    structures: list[IDSStructure] = []

    for op in BINARY_OPS:
        for k in range(1, n):
            left_structures = enumerate_structures(k)
            right_structures = enumerate_structures(n - k)

            for left in left_structures:
                for right in right_structures:
                    structures.append(IDSStructure(op, (left, right)))

    if n >= 3:
        for op in TERNARY_OPS:
            for i in range(1, n - 1):
                for j in range(1, n - i):
                    k = n - i - j
                    if k < 1:
                        continue

                    left_structures = enumerate_structures(i)
                    mid_structures = enumerate_structures(j)
                    right_structures = enumerate_structures(k)

                    for left in left_structures:
                        for mid in mid_structures:
                            for right in right_structures:
                                structures.append(IDSStructure(op, (left, mid, right)))

    return tuple(structures)


def build_ids_string(structure: IDSStructure, radicals: list[str]) -> str:
    """Build an IDS string from a structure and radicals.

    Args:
        structure: The IDS tree structure.
        radicals: List of radical characters (in order of consumption).

    Returns:
        The IDS string (e.g., "⿰金木").

    Raises:
        ValueError: If radical count doesn't match structure's component count.
    """
    expected = structure.component_count
    if len(radicals) != expected:
        raise ValueError(f"Structure requires {expected} radicals, got {len(radicals)}")

    def _build(s: IDSStructure, rad_iter: list[str], idx: list[int]) -> str:
        if s.is_leaf:
            result = rad_iter[idx[0]]
            idx[0] += 1
            return result

        assert s.operator is not None
        parts = [s.operator.symbol]
        for child in s.children:
            parts.append(_build(child, rad_iter, idx))
        return "".join(parts)

    return _build(structure, radicals, [0])
