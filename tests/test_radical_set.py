"""Tests for RadicalSet class - Phase 2 of tensor algebra implementation.

TDD approach: Tests written first, then implementation.
Base cases: n=1 (single radical), n=2 (minimal non-trivial).
"""

import pytest

from radical_algebra.core import RadicalSet
from radical_algebra.exceptions import InvalidRadicalError, SimplifiedChineseError


class TestRadicalSetCreation:
    """Tests for RadicalSet creation with various sizes."""

    def test_should_create_size_1_radical_set(self) -> None:
        """Base case n=1: Single radical set."""
        rs = RadicalSet("單", ["金"])
        assert rs.name == "單"
        assert len(rs) == 1
        assert list(rs) == ["金"]

    def test_should_create_size_2_radical_set(self) -> None:
        """Base case n=2: Minimal non-trivial set."""
        rs = RadicalSet("二元", ["金", "木"])
        assert rs.name == "二元"
        assert len(rs) == 2
        assert list(rs) == ["金", "木"]

    def test_should_create_wu_xing_radical_set(self) -> None:
        """Target case n=5: Wu Xing (Five Elements)."""
        rs = RadicalSet("五行", ["金", "木", "水", "火", "土"])
        assert rs.name == "五行"
        assert len(rs) == 5
        assert list(rs) == ["金", "木", "水", "火", "土"]


class TestRadicalSetValidation:
    """Tests for validation of radicals during RadicalSet creation."""

    def test_should_raise_when_invalid_radical(self) -> None:
        """Invalid ASCII character should raise InvalidRadicalError."""
        with pytest.raises(InvalidRadicalError, match="not a valid CJK character"):
            RadicalSet("bad", ["a"])

    def test_should_raise_when_simplified_radical(self) -> None:
        """Simplified-only character should raise SimplifiedChineseError."""
        with pytest.raises(SimplifiedChineseError, match="simplified Chinese only"):
            RadicalSet("bad", ["车"])

    def test_should_raise_when_empty_radicals(self) -> None:
        """Empty radical list should raise ValueError."""
        with pytest.raises(ValueError, match="at least one radical"):
            RadicalSet("empty", [])

    def test_should_raise_when_duplicate_radicals(self) -> None:
        """Duplicate radicals should raise ValueError."""
        with pytest.raises(ValueError, match="duplicate"):
            RadicalSet("dup", ["金", "金"])


class TestRadicalSetIteration:
    """Tests for iteration over RadicalSet."""

    def test_should_iterate_over_radicals(self) -> None:
        """Should support iteration via __iter__."""
        rs = RadicalSet("test", ["金", "木"])
        radicals = []
        for r in rs:
            radicals.append(r)
        assert radicals == ["金", "木"]

    def test_should_have_length(self) -> None:
        """Should support len() via __len__."""
        rs = RadicalSet("test", ["金", "木", "水"])
        assert len(rs) == 3


class TestRadicalSetIndexing:
    """Tests for index access to RadicalSet."""

    def test_should_access_by_index(self) -> None:
        """Should support index access via __getitem__."""
        rs = RadicalSet("test", ["金", "木", "水"])
        assert rs[0] == "金"
        assert rs[1] == "木"
        assert rs[2] == "水"

    def test_should_raise_on_out_of_bounds(self) -> None:
        """Out of bounds index should raise IndexError."""
        rs = RadicalSet("test", ["金", "木"])
        with pytest.raises(IndexError):
            _ = rs[5]

    def test_should_support_negative_index(self) -> None:
        """Should support negative indexing."""
        rs = RadicalSet("test", ["金", "木", "水"])
        assert rs[-1] == "水"
        assert rs[-2] == "木"
