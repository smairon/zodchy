import typing

T = typing.TypeVar('T')


class IdentifiersFactory(typing.Protocol[T]):
    def random(self) -> T: ...

    def derived(self, value: str | bytes) -> T: ...
