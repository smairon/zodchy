"""
Tests for the toolbox.di module.
"""

import pytest
from typing import Any
from zodchy.toolbox.di import (
    DIResolverContract,
    DIContainerContract,
    DependencyContract,
    DependencyImplementation,
    DependencyContext,
    ShutdownContext,
    ResolverContext,
    DependencyCallbackContext,
    DependencyCallback,
)


class TestDIResolverContract:
    """Test class for DIResolverContract protocol."""

    def test_resolver_contract_has_resolve_method(self):
        """Test that DIResolverContract has resolve method."""
        assert hasattr(DIResolverContract, "resolve")

    def test_resolver_contract_has_shutdown_method(self):
        """Test that DIResolverContract has shutdown method."""
        assert hasattr(DIResolverContract, "shutdown")

    def test_resolver_contract_has_context_manager_methods(self):
        """Test that DIResolverContract has context manager methods."""
        assert hasattr(DIResolverContract, "__aenter__")
        assert hasattr(DIResolverContract, "__aexit__")

    async def test_resolver_implementation(self):
        """Test that a class can implement DIResolverContract."""
        class SimpleResolver:
            def __init__(self, dependencies: dict[type, Any] | None = None):
                self._dependencies = dependencies or {}

            async def resolve(
                self,
                contract: DependencyContract,
                context: DependencyContext | None = None,
            ) -> Any:
                return self._dependencies.get(contract)

            async def shutdown(self, context: ShutdownContext | None = None) -> None:
                pass

            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                return None

        resolver: DIResolverContract = SimpleResolver()
        assert resolver is not None

        # Test resolve
        class TestDependency:
            pass

        test_dep = TestDependency()
        resolver_with_deps = SimpleResolver({TestDependency: test_dep})
        result = await resolver_with_deps.resolve(TestDependency)
        assert result is test_dep

        # Test shutdown
        await resolver.shutdown()

        # Test context manager
        async with resolver:
            pass


class TestDIContainerContract:
    """Test class for DIContainerContract protocol."""

    def test_container_contract_has_register_dependency_method(self):
        """Test that DIContainerContract has register_dependency method."""
        assert hasattr(DIContainerContract, "register_dependency")

    def test_container_contract_has_register_callback_method(self):
        """Test that DIContainerContract has register_callback method."""
        assert hasattr(DIContainerContract, "register_callback")

    def test_container_contract_has_get_resolver_method(self):
        """Test that DIContainerContract has get_resolver method."""
        assert hasattr(DIContainerContract, "get_resolver")

    def test_container_contract_has_shutdown_method(self):
        """Test that DIContainerContract has shutdown method."""
        assert hasattr(DIContainerContract, "shutdown")

    def test_container_contract_has_context_manager_methods(self):
        """Test that DIContainerContract has context manager methods."""
        assert hasattr(DIContainerContract, "__aenter__")
        assert hasattr(DIContainerContract, "__aexit__")

    async def test_container_implementation(self):
        """Test that a class can implement DIContainerContract."""
        class SimpleContainer:
            def __init__(self):
                self._dependencies: dict[type, Any] = {}
                self._callbacks: list[tuple[type, DependencyCallback, str]] = []

            def register_dependency(
                self,
                implementation: DependencyImplementation,
                contract: DependencyContract | None = None,
                cache_scope: str | None = None,
            ) -> None:
                contract_type = contract or type(implementation)
                self._dependencies[contract_type] = implementation

            def register_callback(
                self,
                contract: DependencyContract,
                callback: DependencyCallback,
                trigger: str,
            ) -> None:
                self._callbacks.append((contract, callback, trigger))

            def get_resolver(self, *context: Any) -> DIResolverContract:
                class Resolver:
                    def __init__(self, deps: dict[type, Any]):
                        self._deps = deps

                    async def resolve(
                        self,
                        contract: DependencyContract,
                        context: DependencyContext | None = None,
                    ) -> Any:
                        return self._deps.get(contract)

                    async def shutdown(self, context: ShutdownContext | None = None) -> None:
                        pass

                    async def __aenter__(self):
                        return self

                    async def __aexit__(self, exc_type, exc_val, exc_tb):
                        return None

                return Resolver(self._dependencies)

            async def shutdown(self, context: ShutdownContext | None = None) -> None:
                pass

            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                return None

        container: DIContainerContract = SimpleContainer()
        assert container is not None

        # Test register_dependency
        class TestDependency:
            pass

        test_dep = TestDependency()
        container.register_dependency(test_dep, TestDependency)
        container.register_dependency(test_dep)  # Without explicit contract

        # Test get_resolver
        resolver = container.get_resolver()
        assert resolver is not None
        resolved = await resolver.resolve(TestDependency)
        assert resolved is test_dep

        # Test register_callback
        def callback(contract: DependencyContract, ctx: DependencyCallbackContext) -> None:
            pass

        container.register_callback(TestDependency, callback, "shutdown")

        # Test shutdown
        await container.shutdown()

        # Test context manager
        async with container:
            pass


class TestDITypeAliases:
    """Test class for DI type aliases."""

    def test_dependency_contract_type(self):
        """Test DependencyContract type alias."""
        # DependencyContract should be a type
        class TestClass:
            pass

        contract: DependencyContract = TestClass
        assert contract is TestClass

    def test_dependency_implementation_type(self):
        """Test DependencyImplementation type alias."""
        # DependencyImplementation should be Any
        impl: DependencyImplementation = "string"
        impl = 42
        impl = object()
        assert impl is not None

    def test_dependency_context_type(self):
        """Test DependencyContext type alias."""
        # DependencyContext should be a Mapping
        context: DependencyContext = {}
        context = {str: {}}
        assert isinstance(context, dict)

    def test_shutdown_context_type(self):
        """Test ShutdownContext type alias."""
        # ShutdownContext should be a Mapping
        context: ShutdownContext = {}
        context = {"key": "value"}
        assert isinstance(context, dict)

    def test_resolver_context_type(self):
        """Test ResolverContext type alias."""
        # ResolverContext should be a Mapping
        context: ResolverContext = {}
        context = {"key": "value"}
        assert isinstance(context, dict)

    def test_dependency_callback_context_type(self):
        """Test DependencyCallbackContext type alias."""
        # DependencyCallbackContext should be a Mapping
        context: DependencyCallbackContext = {}
        context = {"key": "value"}
        assert isinstance(context, dict)

    def test_dependency_callback_type(self):
        """Test DependencyCallback type alias."""
        # DependencyCallback should be a Callable
        def callback(contract: DependencyContract, ctx: DependencyCallbackContext) -> None:
            pass

        cb: DependencyCallback = callback
        assert callable(cb)

