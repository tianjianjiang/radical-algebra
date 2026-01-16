"""Custom exceptions for radical-algebra."""


class RadicalAlgebraError(Exception):
    """Base exception for radical-algebra."""


class InvalidRadicalError(RadicalAlgebraError):
    """Raised when a radical is not a valid CJK character."""


class SimplifiedChineseError(RadicalAlgebraError):
    """Raised when a simplified Chinese character is detected."""


class InvalidRankError(RadicalAlgebraError):
    """Raised when tensor rank is outside supported range (2-5)."""
