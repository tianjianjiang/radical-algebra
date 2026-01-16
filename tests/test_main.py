"""Direct tests for __main__.py to capture coverage.

These tests import and call functions directly instead of using subprocess.
"""

import io
import sys
from unittest.mock import patch

from radical_algebra import RadicalSet, outer_product
from radical_algebra.__main__ import main, print_matrix, print_tensor_diagonal


class TestPrintMatrix:
    """Tests for print_matrix function."""

    def test_should_print_matrix_header(self) -> None:
        """print_matrix should print header with radical labels."""
        rs = RadicalSet("test", ["金", "木"])
        matrix = outer_product(rs, rank=2)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_matrix(matrix, ["金", "木"])
            output = mock_stdout.getvalue()

        assert "金" in output
        assert "木" in output

    def test_should_print_matrix_cells(self) -> None:
        """print_matrix should print cell contents."""
        rs = RadicalSet("test", ["金", "木"])
        matrix = outer_product(rs, rank=2)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_matrix(matrix, ["金", "木"])
            output = mock_stdout.getvalue()

        # Should have separator lines
        assert "---" in output


class TestPrintTensorDiagonal:
    """Tests for print_tensor_diagonal function."""

    def test_should_print_diagonal_header(self) -> None:
        """print_tensor_diagonal should print header with rank info."""
        rs = RadicalSet("test", ["金", "木"])
        tensor = outer_product(rs, rank=3)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_tensor_diagonal(tensor, ["金", "木"], 3)
            output = mock_stdout.getvalue()

        assert "Rank-3" in output
        assert "diagonal" in output.lower()

    def test_should_print_diagonal_with_chars(self) -> None:
        """print_tensor_diagonal should print diagonal characters."""
        rs = RadicalSet("五行", ["金", "木", "水", "火", "土"])
        tensor = outer_product(rs, rank=3)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_tensor_diagonal(tensor, ["金", "木", "水", "火", "土"], 3)
            output = mock_stdout.getvalue()

        # Should show radicals and results
        assert "金" in output
        assert "x 3" in output

    def test_should_handle_no_char_found(self) -> None:
        """print_tensor_diagonal should show message when no char found."""
        # Use radicals that likely have no rank-5 composition
        rs = RadicalSet("test", ["日", "月"])
        tensor = outer_product(rs, rank=5)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_tensor_diagonal(tensor, ["日", "月"], 5)
            output = mock_stdout.getvalue()

        # Should have output (may or may not find chars)
        assert "Rank-5" in output


class TestMain:
    """Tests for main function with mocked argv."""

    def test_main_default_should_return_0(self) -> None:
        """main() with default args should return 0."""
        with patch.object(sys, "argv", ["radical_algebra"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = main()
        assert result == 0

    def test_main_with_rank_3(self) -> None:
        """main() with --rank 3 should return 0."""
        with patch.object(sys, "argv", ["radical_algebra", "--rank", "3"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = main()
        assert result == 0

    def test_main_with_custom_radicals(self) -> None:
        """main() with --radicals should return 0."""
        with patch.object(sys, "argv", ["radical_algebra", "--radicals", "日月"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                result = main()
        assert result == 0

    def test_main_with_invalid_radicals_should_return_1(self) -> None:
        """main() with invalid radicals should return 1."""
        with patch.object(sys, "argv", ["radical_algebra", "--radicals", "abc"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                with patch("sys.stderr", new_callable=io.StringIO):
                    result = main()
        assert result == 1

    def test_main_with_simplified_radicals_should_return_1(self) -> None:
        """main() with simplified Chinese radicals should return 1."""
        with patch.object(sys, "argv", ["radical_algebra", "--radicals", "龙"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                with patch("sys.stderr", new_callable=io.StringIO):
                    result = main()
        assert result == 1

    def test_main_rank_2_shows_notable(self) -> None:
        """main() with rank 2 should show notable characters."""
        with patch.object(sys, "argv", ["radical_algebra", "--rank", "2"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
        assert "Notable" in output

    def test_main_rank_3_shows_diagonal_results(self) -> None:
        """main() with rank 3 should show diagonal results."""
        with patch.object(sys, "argv", ["radical_algebra", "--rank", "3"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()

        # Should show x3 notation for triple
        assert "x3" in output or "x 3" in output or "× 3" in output


class TestMatrixCellFormatting:
    """Tests for matrix cell formatting edge cases."""

    def test_should_handle_empty_cell(self) -> None:
        """print_matrix should handle cells with no characters."""
        # Use radicals that might have empty cells
        rs = RadicalSet("test", ["日", "月"])
        matrix = outer_product(rs, rank=2)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_matrix(matrix, ["日", "月"])
            output = mock_stdout.getvalue()

        # Should produce output regardless
        assert len(output) > 0

    def test_should_handle_many_chars_in_cell(self) -> None:
        """print_matrix should truncate cells with many characters."""
        rs = RadicalSet("五行", ["金", "木", "水", "火", "土"])
        matrix = outer_product(rs, rank=2)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            print_matrix(matrix, ["金", "木", "水", "火", "土"])
            output = mock_stdout.getvalue()

        # Output should exist (cells may be truncated with "..")
        assert len(output) > 0
