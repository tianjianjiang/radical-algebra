"""Tests for CJKV validation module."""

import pytest

from radical_algebra.exceptions import InvalidRadicalError, SimplifiedChineseError
from radical_algebra.validation import is_cjk_character, is_simplified_only, validate_radical


class TestIsCjkCharacter:
    """Tests for is_cjk_character function."""

    def test_should_return_true_when_valid_cjk_character(self) -> None:
        """Traditional CJK characters should be valid."""
        assert is_cjk_character("金") is True
        assert is_cjk_character("木") is True
        assert is_cjk_character("水") is True
        assert is_cjk_character("火") is True
        assert is_cjk_character("土") is True
        assert is_cjk_character("龍") is True  # Traditional dragon

    def test_should_return_false_when_ascii_character(self) -> None:
        """ASCII characters should not be valid CJK."""
        assert is_cjk_character("a") is False
        assert is_cjk_character("Z") is False
        assert is_cjk_character("1") is False
        assert is_cjk_character("!") is False

    def test_should_return_false_when_emoji(self) -> None:
        """Emoji should not be valid CJK."""
        assert is_cjk_character("😀") is False
        assert is_cjk_character("🔥") is False

    def test_should_return_false_when_empty_string(self) -> None:
        """Empty string should not be valid."""
        assert is_cjk_character("") is False

    def test_should_return_false_when_multiple_characters(self) -> None:
        """Multiple characters should not be valid (single char only)."""
        assert is_cjk_character("金木") is False

    def test_should_accept_extension_i_character(self) -> None:
        """Extension I characters (Unicode 15.0) should be valid CJK."""
        # U+2EC00 is in Extension I range (U+2EBF0–U+2EE5D)
        assert is_cjk_character("\U0002ec00") is True

    def test_should_accept_extension_j_character(self) -> None:
        """Extension J characters (Unicode 17.0) should be valid CJK."""
        # U+323B0 is first char in Extension J range (U+323B0–U+3347F)
        assert is_cjk_character("\U000323b0") is True

    def test_should_accept_extension_j_upper_boundary(self) -> None:
        """Extension J upper boundary (U+3347F) should be valid."""
        assert is_cjk_character("\U0003347f") is True
        # U+33480 is outside the range
        assert is_cjk_character("\U00033480") is False


class TestIsSimplifiedOnly:
    """Tests for is_simplified_only function."""

    def test_should_detect_simplified_only_character(self) -> None:
        """Characters that exist only in simplified Chinese should be detected."""
        assert is_simplified_only("说") is True  # Simplified of 說
        assert is_simplified_only("龙") is True  # Simplified of 龍

    def test_should_allow_traditional_character(self) -> None:
        """Traditional characters should not be flagged as simplified-only."""
        assert is_simplified_only("說") is False  # Traditional
        assert is_simplified_only("龍") is False  # Traditional dragon

    def test_should_allow_shared_character(self) -> None:
        """Characters shared between traditional and simplified should be allowed."""
        assert is_simplified_only("金") is False  # Same in both systems
        assert is_simplified_only("木") is False
        assert is_simplified_only("水") is False
        assert is_simplified_only("火") is False
        assert is_simplified_only("土") is False


class TestValidateRadical:
    """Tests for validate_radical function."""

    def test_should_pass_when_valid_radical(self) -> None:
        """Valid CJK radicals should pass validation."""
        validate_radical("金")  # Should not raise
        validate_radical("木")
        validate_radical("水")

    def test_should_raise_when_invalid_radical(self) -> None:
        """Non-CJK characters should raise InvalidRadicalError."""
        with pytest.raises(InvalidRadicalError):
            validate_radical("a")
        with pytest.raises(InvalidRadicalError):
            validate_radical("1")
        with pytest.raises(InvalidRadicalError):
            validate_radical("")

    def test_should_raise_when_simplified_radical(self) -> None:
        """Simplified-only characters should raise SimplifiedChineseError."""
        with pytest.raises(SimplifiedChineseError):
            validate_radical("说")
        with pytest.raises(SimplifiedChineseError):
            validate_radical("龙")
