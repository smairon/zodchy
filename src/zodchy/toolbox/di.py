import collections.abc
import typing

DependencyContract: typing.TypeAlias = type
DependencyImplementation: typing.TypeAlias = typing.Any
DependencyContext: typing.TypeAlias = collections.abc.Mapping[str | DependencyContract, typing.Any]
ShutdownContext: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]
ResolverContext: typing.TypeAlias = collections.abc.Mapping[str | DependencyContract, typing.Any]

DependencyCallbackContext: typing.TypeAlias = collections.abc.Mapping[str, typing.Any]


class DependencyCallback(typing.Protocol):
    def __call__(
        self,
        dependency: DependencyImplementation,
        context: DependencyCallbackContext,
    ) -> typing.Any | collections.abc.Awaitable[typing.Any]: ...


class DIResolverContract(typing.Protocol):
    async def resolve(self, contract: DependencyContract, context: ResolverContext | None = None) -> typing.Any: ...

    async def shutdown(self, context: ShutdownContext | None = None) -> None: ...

    async def __aenter__(self) -> typing.Self: ...

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: typing.Any
    ) -> None: ...


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

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: typing.Any
    ) -> None: ...
