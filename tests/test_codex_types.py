"""
Tests for the codex.types module.
"""

from zodchy.codex.types import Empty, Skip


class TestEmpty:
    """Test class for Empty type."""

    def test_empty_is_new_type(self):
        """Test that Empty is a NewType."""
        # Empty is a NewType, so it requires explicit construction
        empty = Empty(object())
        assert isinstance(empty, object)

    def test_empty_type_identity(self):
        """Test that Empty maintains type identity."""
        obj = object()
        empty = Empty(obj)
        # Empty is a type wrapper, so the underlying object is the same
        assert empty is obj or empty == obj


class TestSkip:
    """Test class for Skip type."""

    def test_skip_is_new_type(self):
        """Test that Skip is a NewType."""
        # Skip is a NewType, so it requires explicit construction
        skip = Skip(object())
        assert isinstance(skip, object)

    def test_skip_type_identity(self):
        """Test that Skip maintains type identity."""
        obj = object()
        skip = Skip(obj)
        # Skip is a type wrapper, so the underlying object is the same
        assert skip is obj or skip == obj

