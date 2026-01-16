"""Tests for Character Database - IDS-based character lookup.

Phase 4: Set-based lookup from radical combinations to valid characters.
Key insight: Each radical pair maps to a SET of characters (one per valid IDS pattern).

Updated for Phase 9: Comprehensive cjkvi-ids database integration.
The cjkvi-ids database has 88,937 entries with proper Unicode IDS decompositions.

Phase 12.2: Added parameterized tests for comprehensive radical coverage.
"""

import pytest

from radical_algebra.character_db import CharacterDatabase


class TestCharacterDatabaseBasics:
    """Tests for basic CharacterDatabase functionality."""

    def test_should_create_database(self) -> None:
        """Database should initialize with IDS mappings."""
        db = CharacterDatabase()
        assert db is not None

    def test_should_have_entries(self) -> None:
        """Database should contain IDS->character mappings."""
        db = CharacterDatabase()
        assert len(db) > 0


class TestLookupByIDS:
    """Tests for exact IDS string lookup (returns set of characters)."""

    def test_should_find_char_by_exact_ids_lr(self) -> None:
        """Exact IDS lookup: ⿰金金 -> set containing 鍂."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿰金金")
        assert "鍂" in result

    def test_should_find_lin_by_ids(self) -> None:
        """Exact IDS lookup: ⿰木木 -> set containing 林 or compatibility variant."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿰木木")
        # cjkvi-ids may have U+6797 林 and/or U+F9F4 林 (compatibility ideograph)
        assert "林" in result or "\uf9f4" in result

    def test_should_find_yan_by_ids(self) -> None:
        """Exact IDS lookup: ⿱火火 -> set containing 炎."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿱火火")
        assert "炎" in result

    def test_should_find_gui_by_ids(self) -> None:
        """Exact IDS lookup: ⿱土土 -> set containing 圭."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿱土土")
        assert "圭" in result

    def test_should_return_empty_set_when_ids_not_found(self) -> None:
        """Return empty set for unknown IDS patterns."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿰X X")
        assert result == set()


class TestLookupByComponents:
    """Tests for component-based lookup (returns SET of characters)."""

    def test_should_find_set_when_double_wood(self) -> None:
        """木+木 should return set containing 林."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["木", "木"])
        assert "林" in result

    def test_should_find_set_when_double_fire(self) -> None:
        """火+火 should return set containing 炎."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["火", "火"])
        assert "炎" in result

    def test_should_find_jin2_in_set_when_double_metal(self) -> None:
        """金+金 should return set containing 鍂."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["金", "金"])
        assert "鍂" in result

    def test_should_find_shui2_when_double_water(self) -> None:
        """水+水 should return set containing 沝."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["水", "水"])
        assert "沝" in result

    def test_should_find_gui_when_double_earth(self) -> None:
        """土+土 should return set containing 圭."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["土", "土"])
        assert "圭" in result

    def test_should_return_empty_set_when_no_match(self) -> None:
        """Unknown component combinations return empty set."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["X", "Y"])
        assert result == set()


class TestIDSOperatorDistinction:
    """Tests ensuring different IDS operators yield different results."""

    def test_should_distinguish_lr_from_tb(self) -> None:
        """⿰木木 (林) differs from ⿱木木 (if exists)."""
        db = CharacterDatabase()
        lr_result = db.lookup_by_ids("⿰木木")
        tb_result = db.lookup_by_ids("⿱木木")
        if lr_result and tb_result:
            # Sets should not be identical
            assert lr_result != tb_result

    def test_lin_is_lr_not_tb(self) -> None:
        """林 is specifically left-right composition."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿰木木")
        # Accept both U+6797 林 and U+F9F4 compatibility variant
        assert "林" in result or "\uf9f4" in result


class TestTernaryLookup:
    """Tests for 3-component character lookup using composition-based search.

    Note: Characters like 鑫 have nested IDS (⿱金鍂), so lookup_by_components
    won't find them. We use lookup_by_composition which counts radicals.
    """

    def test_should_find_xin_when_triple_gold(self) -> None:
        """金×3 should return set containing 鑫."""
        db = CharacterDatabase()
        result = db.lookup_by_composition({"金": 3})
        assert "鑫" in result

    def test_should_find_sen_when_triple_wood(self) -> None:
        """木×3 should return set containing 森."""
        db = CharacterDatabase()
        result = db.lookup_by_composition({"木": 3})
        assert "森" in result

    def test_should_find_miao_when_triple_water(self) -> None:
        """水×3 should return set containing 淼."""
        db = CharacterDatabase()
        result = db.lookup_by_composition({"水": 3})
        assert "淼" in result

    def test_should_find_yan3_when_triple_fire(self) -> None:
        """火×3 should return set containing 焱."""
        db = CharacterDatabase()
        result = db.lookup_by_composition({"火": 3})
        assert "焱" in result

    def test_should_find_yao_when_triple_earth(self) -> None:
        """土×3 should return set containing 垚."""
        db = CharacterDatabase()
        result = db.lookup_by_composition({"土": 3})
        assert "垚" in result


class TestOffDiagonalLookup:
    """Tests for off-diagonal (different radicals) lookup."""

    def test_should_find_chars_when_water_gold(self) -> None:
        """水+金 should return set containing valid characters.

        Note: 淦 uses 氵 (three-dot water) not 水, so it won't be found.
        Valid 水+金 characters include 淾, 𨥗, 𫒎.
        """
        db = CharacterDatabase()
        result = db.lookup_by_composition({"水": 1, "金": 1})
        # Should find characters with exactly 1 water + 1 gold radical
        assert len(result) > 0
        # These are actual 水+金 characters in cjkvi-ids
        assert any(c in result for c in ["淾", "𨥗", "𫒎"])

    def test_should_find_chars_when_wood_earth(self) -> None:
        """木+土 should return set containing 杜."""
        db = CharacterDatabase()
        result = db.lookup_by_composition({"木": 1, "土": 1})
        assert "杜" in result


class TestNonWuXingRadicals:
    """Tests for non-Wu Xing radical lookups.

    Phase 12.1: Verify lookup methods work with radicals beyond Wu Xing (五行).
    Uses lookup_by_components which works for any radicals.
    """

    def test_should_find_chang_when_double_sun(self) -> None:
        """日+日 should return set containing 昌."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["日", "日"])
        assert "昌" in result

    def test_should_find_ming_when_sun_moon(self) -> None:
        """日+月 should return set containing 明."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["日", "月"])
        assert "明" in result

    def test_should_find_lv_when_double_mouth(self) -> None:
        """口+口 should return set containing 吕."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["口", "口"])
        assert "吕" in result

    def test_should_find_multiple_chars_for_same_components(self) -> None:
        """Some radical pairs yield multiple characters."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["日", "日"])
        # 日+日 produces 昌, 昍, and possibly more
        assert len(result) >= 2
        assert "昌" in result

    def test_should_find_exact_ids_for_non_wu_xing(self) -> None:
        """Exact IDS lookup works for non-Wu Xing radicals (returns sets)."""
        db = CharacterDatabase()
        assert len(db.lookup_by_ids("⿱日日")) > 0
        assert "明" in db.lookup_by_ids("⿰日月")
        assert "吕" in db.lookup_by_ids("⿱口口")


class TestParameterizedLookups:
    """Parameterized tests for comprehensive radical coverage.

    Phase 12.2: DRY approach to testing many radical combinations.
    """

    @pytest.mark.parametrize(
        "radicals,expected_char",
        [
            # Wu Xing doubles
            (["金", "金"], "鍂"),
            (["木", "木"], "林"),
            (["水", "水"], "沝"),
            (["火", "火"], "炎"),
            (["土", "土"], "圭"),
            # Non-Wu Xing doubles
            (["日", "日"], "昌"),
            (["口", "口"], "吕"),
            (["月", "月"], "朋"),
            (["山", "山"], "屾"),
            (["人", "人"], "从"),
        ],
        ids=[
            "金×2→鍂",
            "木×2→林",
            "水×2→沝",
            "火×2→炎",
            "土×2→圭",
            "日×2→昌",
            "口×2→吕",
            "月×2→朋",
            "山×2→屾",
            "人×2→从",
        ],
    )
    def test_should_find_doubled_radical_chars(
        self, radicals: list[str], expected_char: str
    ) -> None:
        """Doubled radicals should produce expected characters."""
        db = CharacterDatabase()
        result = db.lookup_by_components(radicals)
        assert expected_char in result

    @pytest.mark.parametrize(
        "radical_counts,expected_char",
        [
            # Wu Xing triples (composition-based lookup)
            ({"金": 3}, "鑫"),
            ({"木": 3}, "森"),
            ({"水": 3}, "淼"),
            ({"火": 3}, "焱"),
            ({"土": 3}, "垚"),
        ],
        ids=["金×3→鑫", "木×3→森", "水×3→淼", "火×3→焱", "土×3→垚"],
    )
    def test_should_find_tripled_radical_chars(
        self, radical_counts: dict[str, int], expected_char: str
    ) -> None:
        """Tripled Wu Xing radicals should produce expected characters."""
        db = CharacterDatabase()
        result = db.lookup_by_composition(radical_counts)
        assert expected_char in result

    @pytest.mark.parametrize(
        "radicals,expected_char",
        [
            # Mixed radical pairs
            (["日", "月"], "明"),
            (["女", "子"], "好"),
            (["木", "土"], "杜"),
            (["口", "天"], "吞"),
        ],
        ids=["日+月→明", "女+子→好", "木+土→杜", "口+天→吞"],
    )
    def test_should_find_mixed_radical_chars(self, radicals: list[str], expected_char: str) -> None:
        """Mixed radical pairs should produce expected characters."""
        db = CharacterDatabase()
        result = db.lookup_by_components(radicals)
        assert expected_char in result


class TestUtilityMethods:
    """Tests for utility methods of CharacterDatabase."""

    def test_get_ids_should_return_ids_for_known_char(self) -> None:
        """get_ids should return IDS string for a known character."""
        db = CharacterDatabase()
        # 林 = ⿰木木
        result = db.get_ids("林")
        assert result is not None
        assert "木" in result

    def test_get_ids_should_return_none_for_unknown_char(self) -> None:
        """get_ids should return None for an unknown character."""
        db = CharacterDatabase()
        # ASCII 'a' is not in the database
        result = db.get_ids("a")
        assert result is None

    def test_iter_wu_xing_chars_should_yield_wu_xing_compositions(self) -> None:
        """iter_wu_xing_chars should yield Wu Xing character compositions."""
        db = CharacterDatabase()
        wu_xing_chars = list(db.iter_wu_xing_chars())
        assert len(wu_xing_chars) > 0
        # Each item should be (char, counts_dict)
        char, counts = wu_xing_chars[0]
        assert isinstance(char, str)
        assert isinstance(counts, dict)
        # Counts should only have Wu Xing radicals as keys
        for radical in counts:
            assert radical in ("金", "木", "水", "火", "土")

    def test_iter_wu_xing_chars_should_include_xin(self) -> None:
        """iter_wu_xing_chars should include 鑫 (金×3)."""
        db = CharacterDatabase()
        chars_with_counts = {char: counts for char, counts in db.iter_wu_xing_chars()}
        assert "鑫" in chars_with_counts
        assert chars_with_counts["鑫"] == {"金": 3}
