import typing
import collections.abc
from .bits import ClauseBit

T = typing.TypeVar("T")

NotationParser = typing.Callable[
    [str | collections.abc.Mapping[str, str]],
    collections.abc.Iterable[tuple[str, ClauseBit]]
]
