import typing


class IdentifiersFactory(typing.Protocol):
    def random(self) -> typing.Any: ...

    def derived(self, value: str | bytes) -> typing.Any: ...
