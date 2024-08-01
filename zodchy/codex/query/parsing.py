import typing
import collections.abc
from .bits import ClauseBit

ParamName: typing.TypeAlias = str
ParamValue: typing.TypeAlias = str

NotationQuery: typing.TypeAlias = str | collections.abc.Mapping[ParamName, ParamValue]
NotationTypesMap: typing.TypeAlias = collections.abc.Mapping[ParamName, type]

NotationParser: typing.TypeAlias = typing.Callable[
    [NotationQuery, NotationTypesMap],
    collections.abc.Iterable[tuple[ParamName, ClauseBit]]
]
