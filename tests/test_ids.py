"""Tests for IDS (Ideographic Description Sequence) module.

Phase 3: DP-based enumeration of IDS tree structures.
Mathematical foundation: T(n) counts distinct IDS structures for n components.
"""

import pytest

from radical_algebra.ids import (
    BINARY_OPS,
    TERNARY_OPS,
    build_ids_string,
    enumerate_structures,
)


class TestIDSOperators:
    """Tests for IDS operator constants."""

    def test_should_enumerate_all_binary_operators(self) -> None:
        """Binary operators: 10 total (Unicode 2FF0-2FFB except 2FF2, 2FF3)."""
        assert len(BINARY_OPS) == 10
        expected = ["⿰", "⿱", "⿴", "⿵", "⿶", "⿷", "⿸", "⿹", "⿺", "⿻"]
        assert [op.symbol for op in BINARY_OPS] == expected

    def test_should_enumerate_all_ternary_operators(self) -> None:
        """Ternary operators: 2 total (⿲ left-mid-right, ⿳ top-mid-bottom)."""
        assert len(TERNARY_OPS) == 2
        expected = ["⿲", "⿳"]
        assert [op.symbol for op in TERNARY_OPS] == expected

    def test_binary_ops_should_have_arity_2(self) -> None:
        """All binary operators should have arity 2."""
        for op in BINARY_OPS:
            assert op.arity == 2

    def test_ternary_ops_should_have_arity_3(self) -> None:
        """All ternary operators should have arity 3."""
        for op in TERNARY_OPS:
            assert op.arity == 3


class TestIDSStructureEnumeration:
    """Tests for DP enumeration of IDS tree structures.

    T(n) = number of distinct IDS tree structures for n components.
    T(1) = 1 (identity)
    T(2) = 10 (one for each binary operator)
    T(3) = 10 × (T(1)×T(2) + T(2)×T(1)) + 2 = 202
    """

    def test_should_generate_1_structure_for_n1(self) -> None:
        """T(1) = 1: Identity structure (just the leaf)."""
        structures = enumerate_structures(1)
        assert len(structures) == 1
        assert structures[0].is_leaf

    def test_should_generate_10_structures_for_n2(self) -> None:
        """T(2) = 10: One structure per binary operator."""
        structures = enumerate_structures(2)
        assert len(structures) == 10
        for s in structures:
            assert s.operator is not None
            assert s.operator.arity == 2

    def test_should_generate_202_structures_for_n3(self) -> None:
        """T(3) = 202: 200 nested binary + 2 ternary."""
        structures = enumerate_structures(3)
        assert len(structures) == 202

        binary_count = sum(1 for s in structures if s.operator and s.operator.arity == 2)
        ternary_count = sum(1 for s in structures if s.operator and s.operator.arity == 3)

        assert binary_count == 200  # 10 × (1×10 + 10×1)
        assert ternary_count == 2

    def test_should_raise_when_n_is_zero(self) -> None:
        """n=0 is invalid - no components."""
        with pytest.raises(ValueError, match="at least 1"):
            enumerate_structures(0)

    def test_should_raise_when_n_is_negative(self) -> None:
        """Negative n is invalid."""
        with pytest.raises(ValueError, match="at least 1"):
            enumerate_structures(-1)


class TestIDSStructureProperties:
    """Tests for IDSStructure dataclass properties."""

    def test_leaf_structure_should_have_component_count_1(self) -> None:
        """Leaf structure represents a single component."""
        structures = enumerate_structures(1)
        assert structures[0].component_count == 1

    def test_binary_structure_should_have_component_count_2(self) -> None:
        """Binary structure combines 2 components."""
        structures = enumerate_structures(2)
        for s in structures:
            assert s.component_count == 2

    def test_structure_should_track_depth(self) -> None:
        """Structure depth: leaf=0, binary on leaves=1, nested=2+."""
        leaf_structures = enumerate_structures(1)
        assert leaf_structures[0].depth == 0

        binary_structures = enumerate_structures(2)
        for s in binary_structures:
            assert s.depth == 1

        ternary_structures = [s for s in enumerate_structures(3) if s.operator.arity == 3]
        for s in ternary_structures:
            assert s.depth == 1  # Ternary on 3 leaves


class TestBuildIDSString:
    """Tests for building IDS strings from structures."""

    def test_should_build_ids_string_for_leaf(self) -> None:
        """Leaf structure just returns the radical."""
        structures = enumerate_structures(1)
        result = build_ids_string(structures[0], ["金"])
        assert result == "金"

    def test_should_build_ids_string_for_binary(self) -> None:
        """Binary structure: operator + left + right."""
        structures = enumerate_structures(2)
        lr_structure = next(s for s in structures if s.operator.symbol == "⿰")
        result = build_ids_string(lr_structure, ["金", "木"])
        assert result == "⿰金木"

    def test_should_build_ids_string_for_ternary(self) -> None:
        """Ternary structure: operator + 3 components."""
        structures = enumerate_structures(3)
        lmr_structure = next(s for s in structures if s.operator and s.operator.symbol == "⿲")
        result = build_ids_string(lmr_structure, ["金", "金", "金"])
        assert result == "⿲金金金"

    def test_should_build_ids_string_for_nested_binary(self) -> None:
        """Nested binary: op1(leaf, op2(leaf, leaf))."""
        structures = enumerate_structures(3)
        nested = next(
            s
            for s in structures
            if s.operator and s.operator.arity == 2 and s.children[1].operator is not None
        )
        result = build_ids_string(nested, ["金", "木", "水"])
        assert result.startswith(nested.operator.symbol)
        assert "金" in result and "木" in result and "水" in result

    def test_should_raise_when_radical_count_mismatch(self) -> None:
        """Radical count must match structure's component count."""
        structures = enumerate_structures(2)
        with pytest.raises(ValueError, match="requires 2 radicals"):
            build_ids_string(structures[0], ["金"])

        with pytest.raises(ValueError, match="requires 2 radicals"):
            build_ids_string(structures[0], ["金", "木", "水"])
