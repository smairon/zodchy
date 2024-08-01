import typing
import collections.abc

DependencyContract: typing.TypeAlias = typing.Any
DependencyImplementation: typing.TypeAlias = typing.Any

DependencyCallbackContext: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]
DependencyCallback: typing.TypeAlias = collections.abc.Callable[
    [DependencyContract, DependencyCallbackContext],
    typing.NoReturn
]


class DIResolverContract(typing.Protocol):
    async def resolve(
        self,
        contract: DependencyContract,
        execution_context: collections.abc.Mapping[str, typing.Any] | None = None,
        initial_context: collections.abc.Mapping[str, typing.Any] | None = None
    ): ...

    def add_context(
        self,
        contract: DependencyContract,
        data: collections.abc.Mapping
    ): ...

    async def shutdown(self, exc_type, exc_val): ...

    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...


class DIContainerContract(typing.Protocol):
    def register_dependency(
        self,
        implementation: DependencyImplementation,
        contract: DependencyContract | None = None,
        cache_scope: typing.Literal['container', 'resolver'] | None = None,
    ): ...

    def register_callback(
        self,
        contract: DependencyContract,
        callback: DependencyCallback,
        trigger: typing.Literal['shutdown'],
    ):  ...

    def get_resolver(self) -> DIResolverContract: ...

    async def shutdown(self, exc_type: typing.Any | None = None): ...

    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
