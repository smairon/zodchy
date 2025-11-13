import collections.abc
import typing

from ..codex.operator import ClauseStream

ParamName: typing.TypeAlias = str
ParamValue: typing.TypeAlias = str


class ParserContract(typing.Protocol):
    def __call__(
        self,
        query: str | collections.abc.Mapping[ParamName, ParamValue],
        types_map: collections.abc.Mapping[ParamName, type],
    ) -> ClauseStream: ...
