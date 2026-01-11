"""Tests for Character Database - IDS-based character lookup.

Phase 4: Set-based lookup from radical combinations to valid characters.
Key insight: Each radical pair maps to a SET of characters (one per valid IDS pattern).
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
        """Exact IDS lookup: ⿰木木 -> 林."""
        db = CharacterDatabase()
        result = db.lookup_by_ids("⿰木木")
        assert result == "林"

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
        assert db.lookup_by_ids("⿰木木") == "林"


class TestTernaryLookup:
    """Tests for 3-component character lookup."""

    def test_should_find_xin_when_triple_gold(self) -> None:
        """金×3 should return set containing 鑫."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["金", "金", "金"])
        assert "鑫" in result

    def test_should_find_sen_when_triple_wood(self) -> None:
        """木×3 should return set containing 森."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["木", "木", "木"])
        assert "森" in result

    def test_should_find_miao_when_triple_water(self) -> None:
        """水×3 should return set containing 淼."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["水", "水", "水"])
        assert "淼" in result

    def test_should_find_yan3_when_triple_fire(self) -> None:
        """火×3 should return set containing 焱."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["火", "火", "火"])
        assert "焱" in result

    def test_should_find_yao_when_triple_earth(self) -> None:
        """土×3 should return set containing 垚."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["土", "土", "土"])
        assert "垚" in result


class TestOffDiagonalLookup:
    """Tests for off-diagonal (different radicals) lookup."""

    def test_should_find_chars_when_water_gold(self) -> None:
        """水+金 should return set containing 淦."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["水", "金"])
        assert "淦" in result

    def test_should_find_chars_when_wood_earth(self) -> None:
        """木+土 should return set containing 杜."""
        db = CharacterDatabase()
        result = db.lookup_by_components(["木", "土"])
        assert "杜" in result
