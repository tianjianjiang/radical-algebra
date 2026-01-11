"""Character database for IDS-based character lookup.

This module provides:
- CharacterDatabase class for IDS -> character mapping
- lookup_by_ids(): Exact IDS string lookup
- lookup_by_components(): Component-based lookup returning SET of characters

The database uses embedded IDS mappings for common compositions,
designed to be extensible with external data sources.
"""

from __future__ import annotations

from collections import defaultdict

# Embedded IDS database for Wu Xing (Five Elements) characters
# Format: IDS string -> character
# This covers the essential characters for tensor algebra demo
_EMBEDDED_IDS_DATA: dict[str, str] = {
    # Rank-2: Two-component characters (diagonal)
    "⿰金金": "鍂",  # jin2 (archaic: sound of metal)
    "⿰木木": "林",  # lin (forest)
    "⿰水水": "沝",  # zhui3 (two rivers)
    "⿱火火": "炎",  # yan (flame)
    "⿱土土": "圭",  # gui (ancient jade tablet)
    # Rank-3: Three-component characters (diagonal)
    "⿱金⿰金金": "鑫",  # xin (prosperity, used in names)
    "⿱木⿰木木": "森",  # sen (forest)
    "⿱水⿰水水": "淼",  # miao (vast water)
    "⿱火⿰火火": "焱",  # yan4 (flame, blaze)
    "⿱⿰土土土": "垚",  # yao (high mountains)
    # Off-diagonal: Different components
    "⿰水金": "淦",  # gan (river name; penetrate)
    "⿰木土": "杜",  # du (birch-leaf pear; to stop)
    "⿱水火": "淡",  # dan (insipid, light)
    "⿰金木": "鉢",  # bo (alms bowl) - variant
    "⿰木金": "鉢",  # bo (alms bowl) - same character, symmetric
    "⿱土水": "汢",  # tu (a place name)
    "⿰火木": "杣",  # mian (forestry worker)
    "⿰水土": "汢",  # tu (variant)
    # Additional off-diagonal compositions
    "⿰土木": "杜",  # du (variant ordering)
    "⿰金水": "淦",  # gan (variant ordering)
    "⿱火土": "灶",  # zao (stove, kitchen god)
    "⿱土火": "灶",  # zao (variant)
    "⿰金土": "釷",  # tu (thorium)
    "⿰土金": "釷",  # tu (variant)
    "⿰水木": "沐",  # mu (wash hair, bathe)
    "⿰木水": "沐",  # mu (variant)
}


class CharacterDatabase:
    """Database for looking up characters by IDS composition.

    Supports:
    - Exact IDS string lookup
    - Component-based lookup (returns SET of all matching characters)

    The database is initialized with embedded data for Wu Xing characters,
    with API designed for extension with external data sources.
    """

    def __init__(self, ids_data: dict[str, str] | None = None) -> None:
        """Initialize the character database.

        Args:
            ids_data: Optional custom IDS->character mapping.
                     Defaults to embedded Wu Xing data.
        """
        self._ids_to_char: dict[str, str] = dict(ids_data or _EMBEDDED_IDS_DATA)

        # Build reverse index: sorted component tuple -> set of (IDS, char)
        self._component_index: dict[tuple[str, ...], set[tuple[str, str]]] = defaultdict(set)
        for ids_string, char in self._ids_to_char.items():
            components = self._extract_components(ids_string)
            sorted_key = tuple(sorted(components))
            self._component_index[sorted_key].add((ids_string, char))

    def __len__(self) -> int:
        """Return number of IDS->character mappings."""
        return len(self._ids_to_char)

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

    @staticmethod
    def _extract_components(ids_string: str) -> list[str]:
        """Extract component characters from an IDS string.

        Args:
            ids_string: IDS string like "⿰金金" or "⿱木⿰木木".

        Returns:
            List of component characters (excluding IDS operators).
        """
        # IDS operators are in U+2FF0-2FFB range
        operators = set("⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻")
        return [c for c in ids_string if c not in operators]
