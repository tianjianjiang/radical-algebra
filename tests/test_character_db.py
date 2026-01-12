"""Tests for Character Database - IDS-based character lookup.

Phase 4: Set-based lookup from radical combinations to valid characters.
Key insight: Each radical pair maps to a SET of characters (one per valid IDS pattern).

Updated for Phase 9: Comprehensive cjkvi-ids database integration.
The cjkvi-ids database has 88,937 entries with proper Unicode IDS decompositions.
"""

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
    """Tests for exact IDS string lookup."""

    def test_should_find_char_by_exact_ids_lr(self) -> None:
        """Exact IDS lookup: ⿰金金 -> 鍂."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿰金金")
        assert result == "鍂"

    def test_should_find_lin_by_ids(self) -> None:
        """Exact IDS lookup: ⿰木木 -> 林 (U+6797 or compatibility variant)."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿰木木")
        # cjkvi-ids has both U+6797 林 and U+F9F4 林 (compatibility ideograph)
        assert result in ("林", "\uf9f4")

    def test_should_find_yan_by_ids(self) -> None:
        """Exact IDS lookup: ⿱火火 -> 炎."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿱火火")
        assert result == "炎"

    def test_should_find_gui_by_ids(self) -> None:
        """Exact IDS lookup: ⿱土土 -> 圭."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿱土土")
        assert result == "圭"

    def test_should_return_none_when_ids_not_found(self) -> None:
        """Return None for unknown IDS patterns."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿰X X")
        assert result is None


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
            assert lr_result != tb_result

    def test_lin_is_lr_not_tb(self) -> None:
        """林 is specifically left-right composition."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿰木木")
        # Accept both U+6797 林 and U+F9F4 compatibility variant
        assert result in ("林", "\uf9f4")


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
