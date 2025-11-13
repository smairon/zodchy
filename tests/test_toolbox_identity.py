"""
Tests for the toolbox.identity module.
"""

import pytest
from typing import Any
from zodchy.toolbox.identity import IdentifiersFactoryContract


class TestIdentifiersFactoryContract:
    """Test class for IdentifiersFactoryContract protocol."""

    def test_factory_contract_has_random_method(self):
        """Test that IdentifiersFactoryContract has random method."""
        assert hasattr(IdentifiersFactoryContract, "random")

    def test_factory_contract_has_derived_method(self):
        """Test that IdentifiersFactoryContract has derived method."""
        assert hasattr(IdentifiersFactoryContract, "derived")

    def test_factory_implementation_with_str(self):
        """Test that a class can implement IdentifiersFactoryContract with str."""
        class StringIDFactory:
            def random(self) -> str:
                return "random-id-123"

            def derived(self, value: str | bytes) -> str:
                if isinstance(value, bytes):
                    return value.decode("utf-8")
                return value

        factory: IdentifiersFactoryContract[str] = StringIDFactory()
        assert factory is not None

        random_id = factory.random()
        assert isinstance(random_id, str)
        assert len(random_id) > 0

        derived_id = factory.derived("test-value")
        assert derived_id == "test-value"

        derived_id_bytes = factory.derived(b"test-value")
        assert derived_id_bytes == "test-value"

    def test_factory_implementation_with_int(self):
        """Test that a class can implement IdentifiersFactoryContract with int."""
        class IntIDFactory:
            def random(self) -> int:
                return 12345

            def derived(self, value: str | bytes) -> int:
                if isinstance(value, bytes):
                    return int(value.decode("utf-8"))
                return int(value)

        factory: IdentifiersFactoryContract[int] = IntIDFactory()
        assert factory is not None

        random_id = factory.random()
        assert isinstance(random_id, int)

        derived_id = factory.derived("42")
        assert derived_id == 42

        derived_id_bytes = factory.derived(b"42")
        assert derived_id_bytes == 42

    def test_factory_implementation_with_uuid(self):
        """Test that a class can implement IdentifiersFactoryContract with UUID."""
        import uuid

        class UUIDFactory:
            def random(self) -> uuid.UUID:
                return uuid.uuid4()

            def derived(self, value: str | bytes) -> uuid.UUID:
                if isinstance(value, bytes):
                    return uuid.UUID(value.decode("utf-8"))
                return uuid.UUID(value)

        factory: IdentifiersFactoryContract[uuid.UUID] = UUIDFactory()
        assert factory is not None

        random_id = factory.random()
        assert isinstance(random_id, uuid.UUID)

        test_uuid = uuid.uuid4()
        derived_id = factory.derived(str(test_uuid))
        assert derived_id == test_uuid

