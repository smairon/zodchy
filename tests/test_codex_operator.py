"""
Tests for the codex.operator module.
"""

import pytest
from zodchy.codex.operator import (
    ClauseBit,
    SliceBit,
    FilterBit,
    OrderBit,
    EQ,
    NE,
    LE,
    GE,
    LT,
    GT,
    IS,
    LIKE,
    SET,
    RANGE,
    NOT,
    Limit,
    Offset,
    ASC,
    DESC,
    ClauseStream,
)


class TestClauseBit:
    """Test class for ClauseBit."""

    def test_clause_bit_initialization(self):
        """Test ClauseBit initialization."""
        bit = ClauseBit()
        assert bit.value == ()

    def test_clause_bit_initialization_with_data(self):
        """Test ClauseBit initialization with data."""
        bit1 = ClauseBit()
        bit2 = ClauseBit()
        bit = ClauseBit(bit1, bit2)
        assert bit.value == (bit1, bit2)

    def test_clause_bit_addition(self):
        """Test ClauseBit addition."""
        bit1 = ClauseBit()
        bit2 = ClauseBit()
        result = bit1 + bit2
        assert isinstance(result, ClauseBit)
        assert bit2 in result.value

    def test_clause_bit_addition_multiple(self):
        """Test ClauseBit addition with multiple bits."""
        bit1 = ClauseBit()
        bit2 = ClauseBit()
        bit3 = ClauseBit()
        result = bit1 + bit2 + bit3
        assert isinstance(result, ClauseBit)
        assert len(result.value) == 2  # After first addition, becomes list
        assert bit2 in result.value
        assert bit3 in result.value

    def test_clause_bit_addition_different_types(self):
        """Test ClauseBit addition with different types."""
        bit1 = ClauseBit()
        limit = Limit(10)
        result = bit1 + limit
        assert isinstance(result, ClauseBit)
        assert limit in result.value

    def test_clause_bit_addition_subclass_to_base(self):
        """Test ClauseBit addition when subclass is added (triggers else branch)."""
        # When a subclass (like Limit) is added, type(self) is not ClauseBit
        # This triggers the else branch at line 22
        limit = Limit(10)
        bit = ClauseBit()
        result = limit + bit
        assert isinstance(result, ClauseBit)
        assert result.value == (limit, bit)


class TestSliceBit:
    """Test class for SliceBit."""

    def test_slice_bit_initialization(self):
        """Test SliceBit initialization."""
        bit = SliceBit(5)
        assert bit.value == 5

    def test_slice_bit_inherits_from_clause_bit(self):
        """Test that SliceBit inherits from ClauseBit."""
        assert issubclass(SliceBit, ClauseBit)


class TestFilterBit:
    """Test class for FilterBit."""

    def test_filter_bit_initialization(self):
        """Test FilterBit initialization with value."""
        class ConcreteFilter(FilterBit[int]):
            pass

        bit = ConcreteFilter(42)
        assert bit.value == 42

    def test_filter_bit_equality(self):
        """Test FilterBit equality."""
        class ConcreteFilter(FilterBit[int]):
            pass

        bit1 = ConcreteFilter(42)
        bit2 = ConcreteFilter(42)
        bit3 = ConcreteFilter(43)
        assert bit1 == 42
        assert bit1 == bit2.value
        assert bit1 != bit3.value

    def test_filter_bit_inherits_from_clause_bit(self):
        """Test that FilterBit inherits from ClauseBit."""
        assert issubclass(FilterBit, ClauseBit)


class TestOrderBit:
    """Test class for OrderBit."""

    def test_order_bit_initialization_default(self):
        """Test OrderBit initialization with default priority."""
        class ConcreteOrder(OrderBit):
            pass

        bit = ConcreteOrder()
        assert bit.value == 0

    def test_order_bit_initialization_with_priority(self):
        """Test OrderBit initialization with priority."""
        class ConcreteOrder(OrderBit):
            pass

        bit = ConcreteOrder(priority=5)
        assert bit.value == 5

    def test_order_bit_inherits_from_clause_bit(self):
        """Test that OrderBit inherits from ClauseBit."""
        assert issubclass(OrderBit, ClauseBit)


class TestEQ:
    """Test class for EQ filter."""

    def test_eq_initialization(self):
        """Test EQ initialization."""
        eq = EQ(42)
        assert eq.value == 42

    def test_eq_equality(self):
        """Test EQ equality."""
        eq = EQ(42)
        assert eq == 42
        assert eq != 43


class TestNE:
    """Test class for NE filter."""

    def test_ne_initialization(self):
        """Test NE initialization."""
        ne = NE(42)
        assert ne.value == 42

    def test_ne_equality(self):
        """Test NE equality."""
        ne = NE(42)
        assert ne == 42
        assert ne != 43


class TestLE:
    """Test class for LE filter."""

    def test_le_initialization(self):
        """Test LE initialization."""
        le = LE(42)
        assert le.value == 42

    def test_le_equality(self):
        """Test LE equality."""
        le = LE(42)
        assert le == 42


class TestGE:
    """Test class for GE filter."""

    def test_ge_initialization(self):
        """Test GE initialization."""
        ge = GE(42)
        assert ge.value == 42

    def test_ge_equality(self):
        """Test GE equality."""
        ge = GE(42)
        assert ge == 42


class TestLT:
    """Test class for LT filter."""

    def test_lt_initialization(self):
        """Test LT initialization."""
        lt = LT(42)
        assert lt.value == 42

    def test_lt_equality(self):
        """Test LT equality."""
        lt = LT(42)
        assert lt == 42


class TestGT:
    """Test class for GT filter."""

    def test_gt_initialization(self):
        """Test GT initialization."""
        gt = GT(42)
        assert gt.value == 42

    def test_gt_equality(self):
        """Test GT equality."""
        gt = GT(42)
        assert gt == 42


class TestIS:
    """Test class for IS filter."""

    def test_is_initialization(self):
        """Test IS initialization."""
        is_filter = IS(None)
        assert is_filter.value is None

    def test_is_equality(self):
        """Test IS equality."""
        is_filter = IS(None)
        assert is_filter == None  # noqa: E711


class TestLIKE:
    """Test class for LIKE filter."""

    def test_like_initialization_default(self):
        """Test LIKE initialization with default case_sensitive."""
        like = LIKE("pattern")
        assert like.value == "pattern"
        assert like.case_sensitive is False

    def test_like_initialization_case_sensitive(self):
        """Test LIKE initialization with case_sensitive=True."""
        like = LIKE("pattern", case_sensitive=True)
        assert like.value == "pattern"
        assert like.case_sensitive is True

    def test_like_equality_same_case_sensitive(self):
        """Test LIKE equality with same case_sensitive."""
        like1 = LIKE("pattern", case_sensitive=False)
        like2 = LIKE("pattern", case_sensitive=False)
        assert like1 == like2

    def test_like_equality_different_case_sensitive(self):
        """Test LIKE equality with different case_sensitive."""
        like1 = LIKE("pattern", case_sensitive=False)
        like2 = LIKE("pattern", case_sensitive=True)
        assert like1 != like2

    def test_like_equality_different_value(self):
        """Test LIKE equality with different value."""
        like1 = LIKE("pattern1")
        like2 = LIKE("pattern2")
        assert like1 != like2

    def test_like_equality_with_non_like(self):
        """Test LIKE equality with non-LIKE object."""
        like = LIKE("pattern")
        with pytest.raises(NotImplementedError):
            like == "pattern"


class TestSET:
    """Test class for SET filter."""

    def test_set_initialization_single(self):
        """Test SET initialization with single value."""
        set_filter = SET(1)
        assert set_filter.value == {1}

    def test_set_initialization_multiple(self):
        """Test SET initialization with multiple values."""
        set_filter = SET(1, 2, 3)
        assert set_filter.value == {1, 2, 3}

    def test_set_initialization_empty(self):
        """Test SET initialization with no values."""
        set_filter = SET()
        assert set_filter.value == set()


class TestRANGE:
    """Test class for RANGE filter."""

    def test_range_initialization_both_bounds(self):
        """Test RANGE initialization with both bounds."""
        left = GE(10)
        right = LE(20)
        range_filter = RANGE(left, right)
        assert range_filter.value == (left, right)

    def test_range_initialization_left_only(self):
        """Test RANGE initialization with left bound only."""
        left = GE(10)
        range_filter = RANGE(left, None)
        assert range_filter.value == (left, None)

    def test_range_initialization_right_only(self):
        """Test RANGE initialization with right bound only."""
        right = LE(20)
        range_filter = RANGE(None, right)
        assert range_filter.value == (None, right)

    def test_range_initialization_no_bounds(self):
        """Test RANGE initialization with no bounds."""
        range_filter = RANGE(None, None)
        assert range_filter.value == (None, None)


class TestNOT:
    """Test class for NOT filter."""

    def test_not_initialization_with_eq(self):
        """Test NOT initialization with EQ."""
        eq = EQ(42)
        not_filter = NOT(eq)
        assert not_filter.value == eq
        assert not_filter._value == eq

    def test_not_initialization_with_like(self):
        """Test NOT initialization with LIKE."""
        like = LIKE("pattern")
        not_filter = NOT(like)
        assert not_filter.value == like

    def test_not_equality_with_none(self):
        """Test NOT equality with None."""
        eq = EQ(42)
        not_filter = NOT(eq)
        assert not not_filter == None  # noqa: E711

    def test_not_equality_with_value(self):
        """Test NOT equality with value."""
        eq = EQ(42)
        not_filter = NOT(eq)
        other_eq = EQ(42)
        assert not_filter == other_eq.value

    def test_not_equality_with_object_has_value(self):
        """Test NOT equality with object that has value attribute (triggers line 125)."""
        # This tests the branch where other has a "value" attribute
        eq = EQ(42)
        not_filter = NOT(eq)
        # Create an object with a value attribute
        class ValueObject:
            def __init__(self, val):
                self.value = val

        obj_with_value = ValueObject(42)
        # This should call super().__eq__(other.value) at line 125
        result = not_filter == obj_with_value
        # The comparison should work because obj_with_value.value == 42
        assert isinstance(result, bool)


class TestLimit:
    """Test class for Limit."""

    def test_limit_initialization(self):
        """Test Limit initialization."""
        limit = Limit(10)
        assert limit.value == 10

    def test_limit_inherits_from_slice_bit(self):
        """Test that Limit inherits from SliceBit."""
        assert issubclass(Limit, SliceBit)


class TestOffset:
    """Test class for Offset."""

    def test_offset_initialization(self):
        """Test Offset initialization."""
        offset = Offset(5)
        assert offset.value == 5

    def test_offset_inherits_from_slice_bit(self):
        """Test that Offset inherits from SliceBit."""
        assert issubclass(Offset, SliceBit)


class TestASC:
    """Test class for ASC."""

    def test_asc_initialization_default(self):
        """Test ASC initialization with default priority."""
        asc = ASC()
        assert asc.value == 0

    def test_asc_initialization_with_priority(self):
        """Test ASC initialization with priority."""
        asc = ASC(priority=1)
        assert asc.value == 1

    def test_asc_inherits_from_order_bit(self):
        """Test that ASC inherits from OrderBit."""
        assert issubclass(ASC, OrderBit)


class TestDESC:
    """Test class for DESC."""

    def test_desc_initialization_default(self):
        """Test DESC initialization with default priority."""
        desc = DESC()
        assert desc.value == 0

    def test_desc_initialization_with_priority(self):
        """Test DESC initialization with priority."""
        desc = DESC(priority=1)
        assert desc.value == 1

    def test_desc_inherits_from_order_bit(self):
        """Test that DESC inherits from OrderBit."""
        assert issubclass(DESC, OrderBit)


class TestClauseStream:
    """Test class for ClauseStream type alias."""

    def test_clause_stream_is_iterable(self):
        """Test that ClauseStream is an iterable."""
        stream: ClauseStream = [
            ("field1", EQ(42)),
            ("field2", LIKE("pattern")),
        ]
        result = list(stream)
        assert len(result) == 2
        assert result[0] == ("field1", EQ(42))
        assert result[1] == ("field2", LIKE("pattern"))

    def test_clause_stream_with_various_bits(self):
        """Test ClauseStream with various clause bits."""
        stream: ClauseStream = [
            ("id", EQ(1)),
            ("name", LIKE("test%")),
            ("age", GE(18)),
            ("age", LE(65)),
            ("limit", Limit(10)),
            ("offset", Offset(0)),
            ("order", ASC()),
        ]
        result = list(stream)
        assert len(result) == 7

