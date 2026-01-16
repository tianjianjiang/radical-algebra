"""Integration tests - verifying the README example works.

Phase 8: Final integration tests ensuring public API works as documented.
"""

from radical_algebra import WU_XING, RadicalSet, outer_product


class TestReadmeExample:
    """Tests that the README example works."""

    def test_should_run_readme_example_rank2(self) -> None:
        """README example: Wu Xing rank-2 outer product."""
        # Define Wu Xing elements (from README)
        wuxing = RadicalSet("五行", ["金", "木", "水", "火", "土"])

        # Rank-2: Matrix of two-radical compounds
        matrix = outer_product(wuxing, rank=2)

        # Verify shape
        assert matrix.shape == (5, 5)

        # Verify diagonal elements (from README)
        assert "鍂" in matrix[0, 0]  # 金+金 (⿰金金)
        assert "林" in matrix[1, 1]  # 木+木 (⿰木木)
        assert "沝" in matrix[2, 2]  # 水+水 (⿰水水)
        assert "炎" in matrix[3, 3]  # 火+火 (⿱火火)
        assert "圭" in matrix[4, 4]  # 土+土 (⿱土土)

    def test_should_run_readme_example_rank3(self) -> None:
        """README example: Wu Xing rank-3 outer product."""
        wuxing = RadicalSet("五行", ["金", "木", "水", "火", "土"])

        # Rank-3: Tensor of three-radical compounds
        tensor3 = outer_product(wuxing, rank=3)

        # Verify shape
        assert tensor3.shape == (5, 5, 5)

        # Verify super-diagonal elements (from README)
        assert "鑫" in tensor3[0, 0, 0]  # 金×3
        assert "森" in tensor3[1, 1, 1]  # 木×3
        assert "淼" in tensor3[2, 2, 2]  # 水×3
        assert "焱" in tensor3[3, 3, 3]  # 火×3
        assert "垚" in tensor3[4, 4, 4]  # 土×3


class TestPresets:
    """Tests for preset RadicalSets."""

    def test_wu_xing_preset_should_exist(self) -> None:
        """WU_XING preset should be importable."""
        assert WU_XING is not None
        assert WU_XING.name == "五行"
        assert len(WU_XING) == 5

    def test_wu_xing_preset_should_have_five_elements(self) -> None:
        """WU_XING should contain 金木水火土."""
        assert list(WU_XING) == ["金", "木", "水", "火", "土"]


class TestPublicAPI:
    """Tests for public API exports."""

    def test_should_import_core_classes(self) -> None:
        """Core classes should be importable from package root."""
        from radical_algebra import RadicalSet, TensorResult

        assert RadicalSet is not None
        assert TensorResult is not None

    def test_should_import_functions(self) -> None:
        """Functions should be importable from package root."""
        from radical_algebra import outer_product

        assert callable(outer_product)

    def test_should_import_exceptions(self) -> None:
        """Exceptions should be importable from package root."""
        from radical_algebra import (
            InvalidRadicalError,
            InvalidRankError,
            RadicalAlgebraError,
            SimplifiedChineseError,
        )

        assert issubclass(InvalidRadicalError, RadicalAlgebraError)
        assert issubclass(SimplifiedChineseError, RadicalAlgebraError)
        assert issubclass(InvalidRankError, RadicalAlgebraError)

    def test_should_have_version(self) -> None:
        """Package should expose version."""
        from radical_algebra import __version__

        assert __version__ == "0.1.0"
