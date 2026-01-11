"""Tests for tensor operations - outer product of radicals.

Phase 5: Rank-2 tensor (2×2 base case)
Phase 6: Scale to 5×5
Phase 7: Higher ranks (3-5)

Key insight: Each tensor cell is a SET of valid characters.
"""

import pytest

from radical_algebra.core import RadicalSet
from radical_algebra.exceptions import InvalidRankError
from radical_algebra.tensor import outer_product


class TestTensorBasics:
    """Tests for basic tensor creation."""

    def test_should_create_tensor_result(self) -> None:
        """TensorResult should store shape and data."""
        rs = RadicalSet("test", ["金", "木"])
        result = outer_product(rs, rank=2)
        assert result is not None
        assert result.shape == (2, 2)

    def test_should_have_radical_set_reference(self) -> None:
        """TensorResult should reference the original RadicalSet."""
        rs = RadicalSet("test", ["金", "木"])
        result = outer_product(rs, rank=2)
        assert result.radical_set is rs


class TestRank2TwoByTwo:
    """Tests for 2×2 rank-2 tensor (base case)."""

    def test_should_return_2x2_matrix_when_rank2_size2(self) -> None:
        """Base case: v = [金, 木] → 2×2 matrix."""
        rs = RadicalSet("二元", ["金", "木"])
        result = outer_product(rs, rank=2)
        assert result.shape == (2, 2)

    def test_should_have_jin2_at_0_0(self) -> None:
        """[0,0]: 金+金 should contain 鍂."""
        rs = RadicalSet("二元", ["金", "木"])
        result = outer_product(rs, rank=2)
        cell_00 = result[0, 0]
        assert "鍂" in cell_00

    def test_should_have_lin_at_1_1(self) -> None:
        """[1,1]: 木+木 should contain 林."""
        rs = RadicalSet("二元", ["金", "木"])
        result = outer_product(rs, rank=2)
        cell_11 = result[1, 1]
        assert "林" in cell_11

    def test_diagonal_cells_should_be_sets(self) -> None:
        """Each cell should be a set of characters."""
        rs = RadicalSet("二元", ["金", "木"])
        result = outer_product(rs, rank=2)
        assert isinstance(result[0, 0], set)
        assert isinstance(result[1, 1], set)

    def test_off_diagonal_should_be_sets(self) -> None:
        """Off-diagonal cells should also be sets."""
        rs = RadicalSet("二元", ["金", "木"])
        result = outer_product(rs, rank=2)
        assert isinstance(result[0, 1], set)
        assert isinstance(result[1, 0], set)


class TestOrderSensitivity:
    """Tests ensuring order matters in tensor composition."""

    def test_should_distinguish_order_in_off_diagonal(self) -> None:
        """[i,j] and [j,i] may have different results (order matters)."""
        rs = RadicalSet("test", ["水", "金"])
        result = outer_product(rs, rank=2)
        # 水+金 (⿰水金) vs 金+水 (⿰金水) may differ
        cell_01 = result[0, 1]  # 水+金
        cell_10 = result[1, 0]  # 金+水
        # Both should be sets (may or may not be equal)
        assert isinstance(cell_01, set)
        assert isinstance(cell_10, set)


class TestRankValidation:
    """Tests for rank validation."""

    def test_should_raise_when_rank_less_than_2(self) -> None:
        """Rank must be at least 2."""
        rs = RadicalSet("test", ["金", "木"])
        with pytest.raises(InvalidRankError, match="between 2 and 5"):
            outer_product(rs, rank=1)

    def test_should_raise_when_rank_greater_than_5(self) -> None:
        """Rank must be at most 5."""
        rs = RadicalSet("test", ["金", "木"])
        with pytest.raises(InvalidRankError, match="between 2 and 5"):
            outer_product(rs, rank=6)


class TestTensorIndexing:
    """Tests for tensor indexing."""

    def test_should_support_tuple_indexing(self) -> None:
        """Should access cells via tuple index."""
        rs = RadicalSet("test", ["金", "木"])
        result = outer_product(rs, rank=2)
        cell = result[0, 0]
        assert isinstance(cell, set)

    def test_should_raise_on_invalid_index(self) -> None:
        """Out of bounds index should raise IndexError."""
        rs = RadicalSet("test", ["金", "木"])
        result = outer_product(rs, rank=2)
        with pytest.raises(IndexError):
            _ = result[5, 5]


class TestWuXingRank2:
    """Tests for Wu Xing (5×5) rank-2 tensor - Phase 6 preview."""

    def test_should_return_5x5_matrix_when_rank2_size5(self) -> None:
        """Wu Xing: v = [金, 木, 水, 火, 土] → 5×5 matrix."""
        rs = RadicalSet("五行", ["金", "木", "水", "火", "土"])
        result = outer_product(rs, rank=2)
        assert result.shape == (5, 5)

    def test_should_have_expected_diagonal_chars(self) -> None:
        """Diagonal should contain: 鍂, 林, 沝, 炎, 圭."""
        rs = RadicalSet("五行", ["金", "木", "水", "火", "土"])
        result = outer_product(rs, rank=2)

        assert "鍂" in result[0, 0]  # 金+金
        assert "林" in result[1, 1]  # 木+木
        assert "沝" in result[2, 2]  # 水+水
        assert "炎" in result[3, 3]  # 火+火
        assert "圭" in result[4, 4]  # 土+土

    def test_should_have_gan_at_water_gold(self) -> None:
        """[2,0]: 水+金 should contain 淦."""
        rs = RadicalSet("五行", ["金", "木", "水", "火", "土"])
        result = outer_product(rs, rank=2)
        # Indices: 金=0, 木=1, 水=2, 火=3, 土=4
        cell = result[2, 0]  # 水+金
        assert "淦" in cell

    def test_should_have_du_at_wood_earth(self) -> None:
        """[1,4]: 木+土 should contain 杜."""
        rs = RadicalSet("五行", ["金", "木", "水", "火", "土"])
        result = outer_product(rs, rank=2)
        cell = result[1, 4]  # 木+土
        assert "杜" in cell
