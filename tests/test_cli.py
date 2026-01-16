"""Tests for CLI module (__main__.py)."""

import subprocess
import sys


class TestCLIDefault:
    """Tests for default CLI invocation."""

    def test_should_run_with_defaults(self) -> None:
        """Default invocation should work (Wu Xing, rank 2)."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert "Wu Xing" in result.stdout or "Five Elements" in result.stdout
        assert "Rank: 2" in result.stdout

    def test_should_show_help(self) -> None:
        """--help should show usage information."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "--rank" in result.stdout
        assert "--radicals" in result.stdout


class TestCLIRank:
    """Tests for CLI rank argument."""

    def test_should_accept_rank_3(self) -> None:
        """--rank 3 should work."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--rank", "3"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert "Rank: 3" in result.stdout
        assert "diagonal" in result.stdout.lower()

    def test_should_accept_rank_8(self) -> None:
        """--rank 8 should work (highest supported)."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--rank", "8"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0
        assert "Rank: 8" in result.stdout

    def test_should_reject_rank_1(self) -> None:
        """--rank 1 should be rejected by argparse."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--rank", "1"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode != 0
        assert result.stderr  # argparse error message (format varies by Python version)

    def test_should_reject_rank_9(self) -> None:
        """--rank 9 should be rejected by argparse."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--rank", "9"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode != 0
        assert result.stderr  # argparse error message (format varies by Python version)


class TestCLICustomRadicals:
    """Tests for CLI custom radicals argument."""

    def test_should_accept_custom_radicals(self) -> None:
        """--radicals should accept custom CJK characters."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--radicals", "日月"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert "custom" in result.stdout.lower()
        assert "日" in result.stdout
        assert "月" in result.stdout

    def test_should_reject_invalid_radicals(self) -> None:
        """--radicals with non-CJK should fail."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--radicals", "abc"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 1
        assert "Error" in result.stderr or "not a valid CJK" in result.stderr

    def test_should_reject_simplified_radicals(self) -> None:
        """--radicals with simplified Chinese should fail."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--radicals", "龙"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 1
        assert "simplified" in result.stderr.lower() or "Error" in result.stderr


class TestCLIOutput:
    """Tests for CLI output format."""

    def test_should_show_notable_characters(self) -> None:
        """Output should include 'Notable characters' section."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        assert "Notable characters" in result.stdout

    def test_rank2_should_show_matrix_format(self) -> None:
        """Rank-2 output should show matrix-like format."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--rank", "2"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        # Matrix format has header row with radicals
        assert "金" in result.stdout
        assert "木" in result.stdout

    def test_rank3_should_show_diagonal_format(self) -> None:
        """Rank-3+ output should show diagonal format."""
        result = subprocess.run(
            [sys.executable, "-m", "radical_algebra", "--rank", "3"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        # Diagonal format shows "x 3" for triple
        assert "x 3" in result.stdout
