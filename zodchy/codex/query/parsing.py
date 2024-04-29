import typing
import collections.abc
from .bits import ClauseBit

T = typing.TypeVar("T")
ParamNameType = str
ParamValueType = str

QueryType = str | collections.abc.Mapping[ParamNameType, ParamValueType]
TypesMapType = collections.abc.Mapping[ParamNameType, type]

NotationParser = typing.Callable[
    [QueryType, TypesMapType],
    collections.abc.Iterable[tuple[ParamNameType, ClauseBit]]
]
