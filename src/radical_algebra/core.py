"""Core classes for radical-algebra."""

from collections.abc import Iterator

from radical_algebra.validation import validate_radical


class RadicalSet:
    """A named collection of CJK radicals for tensor operations.

    Attributes:
        name: Human-readable name for this set (e.g., "五行").
        radicals: List of validated CJK radicals.
    """

    def __init__(self, name: str, radicals: list[str]) -> None:
        """Create a RadicalSet with validated radicals.

        Args:
            name: A human-readable name for this radical set.
            radicals: List of CJK characters to use as radicals.

        Raises:
            ValueError: If radicals list is empty or contains duplicates.
            InvalidRadicalError: If any radical is not a valid CJK character.
            SimplifiedChineseError: If any radical is simplified-only.
        """
        if not radicals:
            raise ValueError("RadicalSet requires at least one radical")

        if len(radicals) != len(set(radicals)):
            raise ValueError("RadicalSet cannot contain duplicate radicals")

        for radical in radicals:
            validate_radical(radical)

        self._name = name
        self._radicals = list(radicals)

    @property
    def name(self) -> str:
        """The human-readable name of this radical set."""
        return self._name

    def __len__(self) -> int:
        """Return the number of radicals in this set."""
        return len(self._radicals)

    def __iter__(self) -> Iterator[str]:
        """Iterate over the radicals in order."""
        return iter(self._radicals)

    def __getitem__(self, index: int) -> str:
        """Get a radical by index.

        Args:
            index: The index of the radical (supports negative indexing).

        Returns:
            The radical at the given index.

        Raises:
            IndexError: If the index is out of bounds.
        """
        return self._radicals[index]

    def __repr__(self) -> str:
        """Return a string representation of this RadicalSet."""
        return f"RadicalSet({self._name!r}, {self._radicals!r})"
