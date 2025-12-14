"""
Tests for the codex.types module.
"""

from zodchy.codex.types import Empty, NoValueType, SkipType


class TestEmpty:
    """Test class for Empty type."""

    def test_empty_is_type_alias(self):
        """Test that Empty is a TypeAlias for NoValue."""
        # Empty is a TypeAlias for NoValue
        assert Empty is NoValueType

    def test_empty_instantiation(self):
        """Test that Empty can be instantiated."""
        empty = Empty()
        assert isinstance(empty, NoValueType)


class TestSkip:
    """Test class for Skip type."""

    def test_skip_is_class(self):
        """Test that Skip is a class."""
        assert isinstance(SkipType, type)

    def test_skip_instantiation(self):
        """Test that Skip can be instantiated."""
        skip = SkipType()
        assert isinstance(skip, SkipType)
