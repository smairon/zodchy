import typing
import collections.abc
from .communication import Command, Query, EventStream

CQProcessor = collections.abc.Callable[[Command | Query], EventStream]
CQProcessorContext = collections.abc.Mapping[typing.Any, typing.Any]


class CQRSFactory(typing.Protocol):
    async def get_processor(
        self,
        context: CQProcessorContext | None = None
    ) -> CQProcessor: ...
