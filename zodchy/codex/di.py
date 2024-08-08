import typing
import collections.abc

DependencyContract: typing.TypeAlias = type
DependencyImplementation: typing.TypeAlias = typing.Any
DependencyContext: typing.TypeAlias = collections.abc.Mapping[DependencyContract, collections.abc.Mapping]
ShutdownContext: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]
ResolverContext: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]

DependencyCallbackContext: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]
DependencyCallback: typing.TypeAlias = collections.abc.Callable[
    [DependencyContract, DependencyCallbackContext],
    typing.NoReturn
]


class DIResolverContract(typing.Protocol):
    async def resolve(
        self,
        contract: DependencyContract,
        context: DependencyContext | None = None
    ): ...

    async def shutdown(self, context: ShutdownContext | None = None): ...

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

    def get_resolver(self, context: ResolverContext) -> DIResolverContract: ...

    async def shutdown(self, context: ShutdownContext | None = None): ...

    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
