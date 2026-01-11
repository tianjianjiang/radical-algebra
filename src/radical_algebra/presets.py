"""Preset radical sets for common use cases.

This module provides ready-to-use RadicalSet instances for
well-known character sets like Wu Xing (Five Elements).
"""

from radical_algebra.core import RadicalSet

# Wu Xing (五行) - The Five Elements
# Metal, Wood, Water, Fire, Earth
WU_XING = RadicalSet("五行", ["金", "木", "水", "火", "土"])
