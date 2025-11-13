import collections.abc
import typing

DependencyContract: typing.TypeAlias = type
DependencyImplementation: typing.TypeAlias = typing.Any
DependencyContext: typing.TypeAlias = collections.abc.Mapping[DependencyContract, collections.abc.Mapping]
ShutdownContext: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]
ResolverContext: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]

DependencyCallbackContext: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]
DependencyCallback: typing.TypeAlias = collections.abc.Callable[
    [DependencyContract, DependencyCallbackContext], typing.NoReturn
]


class DIResolverContract(typing.Protocol):
    async def resolve(self, contract: DependencyContract, context: DependencyContext | None = None) -> typing.Any: ...

    async def shutdown(self, context: ShutdownContext | None = None) -> None: ...

    async def __aenter__(self) -> typing.Self: ...

    async def __aexit__(self, exc_type: typing.Type[BaseException] | None, exc_val: BaseException | None, exc_tb: typing.Any) -> None: ...


class DIContainerContract(typing.Protocol):
    def register_dependency(
        self,
        implementation: DependencyImplementation,
        contract: DependencyContract | None = None,
        cache_scope: typing.Literal["container", "resolver"] | None = None,
    ) -> None: ...

    def register_callback(
        self,
        contract: DependencyContract,
        callback: DependencyCallback,
        trigger: typing.Literal["shutdown"],
    ) -> None: ...

    def get_resolver(
        self,
        *context: typing.Any,
    ) -> DIResolverContract: ...

    async def shutdown(self, context: ShutdownContext | None = None) -> None: ...

    async def __aenter__(self) -> typing.Self: ...

    async def __aexit__(self, exc_type: typing.Type[BaseException] | None, exc_val: BaseException | None, exc_tb: typing.Any) -> None: ...
