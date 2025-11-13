import typing

T = typing.TypeVar("T")


class IdentifiersFactoryContract(typing.Protocol[T]):  # type: ignore[misc]
    def random(self) -> T: ...

    def derived(self, value: str | bytes) -> T: ...
