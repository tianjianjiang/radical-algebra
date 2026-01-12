"""Character database for IDS-based character lookup.

This module provides:
- CharacterDatabase class for IDS -> character mapping
- lookup_by_ids(): Exact IDS string lookup
- lookup_by_components(): Component-based lookup returning SET of characters
- lookup_by_composition(): Composition-based lookup by radical counts

The database loads from cjkvi-ids for comprehensive coverage (88,937 entries).
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

# IDS operators in U+2FF0-2FFB range
IDS_OPERATORS = frozenset("⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻")

# Wu Xing (Five Elements) radicals
WU_XING_RADICALS = frozenset(["金", "木", "水", "火", "土"])


def _load_cjkvi_ids() -> dict[str, str]:
    """Load IDS data from cjkvi-ids database.

    Returns:
        Dictionary mapping character to IDS decomposition.
    """
    data_path = Path(__file__).parent / "data" / "cjkvi-ids.txt"
    if not data_path.exists():
        return {}

    ids_data: dict[str, str] = {}
    with data_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                char = parts[1]
                # Remove source variant markers like [GJK]
                ids = parts[2].split("[")[0].strip()
                if ids:
                    ids_data[char] = ids
    return ids_data


def _count_wu_xing_radicals(
    char: str,
    ids_data: dict[str, str],
    stop_radicals: frozenset[str] = WU_XING_RADICALS,
    depth: int = 0,
) -> dict[str, int] | None:
    """Count Wu Xing radicals by recursively expanding IDS.

    Args:
        char: Character to analyze.
        ids_data: Dictionary mapping characters to IDS decompositions.
        stop_radicals: Set of radicals to stop expansion at.
        depth: Current recursion depth (prevents infinite loops).

    Returns:
        Dictionary of {radical: count} if char is composed only of stop_radicals,
        None if char contains non-stop radicals.
    """
    if depth > 10:
        return None

    # If this character is a stop radical, return it
    if char in stop_radicals:
        return {char: 1}

    # Get IDS decomposition
    ids = ids_data.get(char, "")
    if not ids or ids[0] not in IDS_OPERATORS:
        # Not decomposable or is a basic character (not Wu Xing)
        return None

    # Recursively count radicals in components
    result: dict[str, int] = defaultdict(int)
    for c in ids:
        if c in IDS_OPERATORS:
            continue
        sub_counts = _count_wu_xing_radicals(c, ids_data, stop_radicals, depth + 1)
        if sub_counts is None:
            # Contains non-Wu Xing radicals
            return None
        for radical, count in sub_counts.items():
            result[radical] += count

    return dict(result) if result else None


class CharacterDatabase:
    """Database for looking up characters by IDS composition.

    Supports:
    - Exact IDS string lookup
    - Component-based lookup (returns SET of all matching characters)
    - Composition-based lookup by radical counts

    The database loads from cjkvi-ids for comprehensive coverage.
    """

    def __init__(self, ids_data: dict[str, str] | None = None) -> None:
        """Initialize the character database.

        Args:
            ids_data: Optional custom IDS->character mapping.
                     Defaults to loading from cjkvi-ids.
        """
        # Load IDS data: character -> IDS decomposition
        self._char_to_ids: dict[str, str] = dict(ids_data) if ids_data else _load_cjkvi_ids()

        # Build reverse index: IDS string -> character
        self._ids_to_char: dict[str, str] = {ids: char for char, ids in self._char_to_ids.items()}

        # Build component index: sorted component tuple -> set of (IDS, char)
        self._component_index: dict[tuple[str, ...], set[tuple[str, str]]] = defaultdict(set)
        for char, ids in self._char_to_ids.items():
            components = self._extract_components(ids)
            sorted_key = tuple(sorted(components))
            self._component_index[sorted_key].add((ids, char))

        # Build Wu Xing composition index: radical_counts -> set of chars
        self._wu_xing_index: dict[tuple[tuple[str, int], ...], set[str]] = defaultdict(set)
        self._build_wu_xing_index()

    def _build_wu_xing_index(self) -> None:
        """Build index of characters by Wu Xing radical composition."""
        for char in self._char_to_ids:
            counts = _count_wu_xing_radicals(char, self._char_to_ids)
            if counts:
                # Create frozen key from counts
                key = tuple(sorted(counts.items()))
                self._wu_xing_index[key].add(char)

    def __len__(self) -> int:
        """Return number of character entries."""
        return len(self._char_to_ids)

    def lookup_by_ids(self, ids_string: str) -> str | None:
        """Look up a character by exact IDS string.

        Args:
            ids_string: The IDS string (e.g., "⿰金金").

        Returns:
            The character if found, None otherwise.
        """
        return self._ids_to_char.get(ids_string)

    def lookup_by_components(self, components: list[str]) -> set[str]:
        """Look up all characters containing exactly these components.

        Args:
            components: List of radical components.

        Returns:
            Set of characters that can be formed from these components.
            Empty set if no matches found.
        """
        sorted_key = tuple(sorted(components))
        entries = self._component_index.get(sorted_key, set())
        return {char for _, char in entries}

    def lookup_by_composition(self, radical_counts: dict[str, int]) -> set[str]:
        """Look up all characters with exactly these radical counts.

        This is the key method for finding ALL characters composed of
        specific Wu Xing radicals, regardless of arrangement.

        Args:
            radical_counts: Dictionary of {radical: count}.
                           E.g., {"金": 2} for 金×2, {"木": 3} for 木×3.

        Returns:
            Set of characters matching this composition.
            E.g., {"鍂"} for 金×2, {"森"} for 木×3.
        """
        key = tuple(sorted(radical_counts.items()))
        return self._wu_xing_index.get(key, set())

    def get_ids(self, char: str) -> str | None:
        """Get the IDS decomposition for a character.

        Args:
            char: The character to look up.

        Returns:
            The IDS string if found, None otherwise.
        """
        return self._char_to_ids.get(char)

    def iter_wu_xing_chars(self) -> Iterator[tuple[str, dict[str, int]]]:
        """Iterate over all characters composed of Wu Xing radicals.

        Yields:
            Tuples of (character, radical_counts).
        """
        for key, chars in self._wu_xing_index.items():
            counts = dict(key)
            for char in chars:
                yield char, counts

    @staticmethod
    def _extract_components(ids_string: str) -> list[str]:
        """Extract component characters from an IDS string.

        Args:
            ids_string: IDS string like "⿰金金" or "⿱木⿰木木".

        Returns:
            List of component characters (excluding IDS operators).
        """
        return [c for c in ids_string if c not in IDS_OPERATORS]
