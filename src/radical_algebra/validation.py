"""CJKV character validation utilities."""

import hanzidentifier

from radical_algebra.exceptions import InvalidRadicalError, SimplifiedChineseError


def is_cjk_character(char: str) -> bool:
    """Check if a single character is a valid CJK ideograph.

    Args:
        char: A single character to check.

    Returns:
        True if the character is in CJK Unicode ranges, False otherwise.
    """
    if len(char) != 1:
        return False

    code_point = ord(char)

    cjk_ranges = [
        (0x4E00, 0x9FFF),  # CJK Unified Ideographs
        (0x3400, 0x4DBF),  # CJK Unified Ideographs Extension A
        (0x20000, 0x2A6DF),  # CJK Unified Ideographs Extension B
        (0x2A700, 0x2B73F),  # CJK Unified Ideographs Extension C
        (0x2B740, 0x2B81F),  # CJK Unified Ideographs Extension D
        (0x2B820, 0x2CEAF),  # CJK Unified Ideographs Extension E
        (0x2CEB0, 0x2EBEF),  # CJK Unified Ideographs Extension F
        (0x2EBF0, 0x2EE5D),  # CJK Unified Ideographs Extension I (Unicode 15.0)
        (0x30000, 0x3134F),  # CJK Unified Ideographs Extension G
        (0x31350, 0x323AF),  # CJK Unified Ideographs Extension H
        (0x323B0, 0x3347B),  # CJK Unified Ideographs Extension J (Unicode 17.0)
    ]

    return any(start <= code_point <= end for start, end in cjk_ranges)


def is_simplified_only(char: str) -> bool:
    """Check if a character is simplified Chinese only (not traditional).

    Args:
        char: A single CJK character to check.

    Returns:
        True if the character is simplified-only, False if traditional or shared.
    """
    if len(char) != 1:
        return False

    result = hanzidentifier.identify(char)
    return result == hanzidentifier.SIMPLIFIED


def validate_radical(char: str) -> None:
    """Validate that a character is a valid CJKV radical (excluding simplified).

    Args:
        char: A single character to validate.

    Raises:
        InvalidRadicalError: If the character is not a valid CJK ideograph.
        SimplifiedChineseError: If the character is simplified-only.
    """
    if not is_cjk_character(char):
        raise InvalidRadicalError(f"'{char}' is not a valid CJK character")

    if is_simplified_only(char):
        raise SimplifiedChineseError(f"'{char}' is simplified Chinese only")
