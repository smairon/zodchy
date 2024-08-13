import collections.abc
import typing

from .messages import (
    Message,
    Command,
    Query,
    Error,
    BDEvent,
    IOEvent,
    Frame
)

P = typing.ParamSpec('P')

Actor = collections.abc.Callable[
    typing.Concatenate[Message | Frame, P],
    Message | collections.abc.Iterable[Message] | None
]
DomainActor = collections.abc.Callable[
    typing.Concatenate[Command, P],
    BDEvent | collections.abc.Iterable[BDEvent]
]
WriteActor = collections.abc.Callable[
    typing.Concatenate[BDEvent, P],
    IOEvent | collections.abc.Iterable[IOEvent] | Error | None
]
ReadActor = collections.abc.Callable[
    typing.Concatenate[Query, P],
    IOEvent | collections.abc.Iterable[IOEvent] | Error
]
AuditActor = collections.abc.Callable[
    typing.Concatenate[Command | Query, P],
    Command | Query | Error
]
