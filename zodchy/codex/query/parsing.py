import typing
import collections.abc
from .bits import ClauseBit

T = typing.TypeVar("T")


class Param(typing.Generic[T]):
    def __init__(self, name: str, value: ClauseBit[T]):
        self._value = value
        self._name = name

    @property
    def value(self) -> ClauseBit:
        return self._value

    @property
    def name(self) -> str:
        return self._name


NotationParser = typing.Callable[
    [str | collections.abc.Mapping[str, str]],
    collections.abc.Iterable[Param]
]
