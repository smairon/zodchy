import typing
import collections.abc

ContractType = typing.Any
ImplementationType = typing.Any

CallbackContextType = collections.abc.Mapping[str, typing.Any]
CallbackType = collections.abc.Callable[[ContractType, CallbackContextType], typing.NoReturn]


class DIResolverContract(typing.Protocol):
    async def resolve(
        self,
        contract: ContractType,
        execution_context: collections.abc.Mapping[str, typing.Any] | None = None,
        initial_context: collections.abc.Mapping[str, typing.Any] | None = None
    ): ...

    def add_context(
        self,
        contract: ContractType,
        data: collections.abc.Mapping
    ): ...

    async def shutdown(self, exc_type, exc_val): ...

    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...


class DIContainerContract(typing.Protocol):
    def register_dependency(
        self,
        implementation: ImplementationType,
        contract: ContractType | None = None,
        cache_scope: typing.Literal['container', 'resolver'] | None = None,
    ): ...

    def register_callback(
        self,
        contract: ContractType,
        callback: CallbackType,
        trigger: typing.Literal['shutdown'],
    ):  ...

    def get_resolver(self) -> DIResolverContract: ...

    async def shutdown(self, exc_type: typing.Any | None = None): ...

    async def __aenter__(self): ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
