import collections.abc
from .messages import (
    Message,
    Command,
    Query,
    Error,
    BDEvent,
    IOEvent,
    Frame
)

Actor = collections.abc.Callable[[Message | Frame, ...], Message | collections.abc.Iterable[Message] | None]
DomainActor = collections.abc.Callable[[Command, ...], BDEvent | collections.abc.Iterable[BDEvent]]
WriteActor = collections.abc.Callable[[BDEvent, ...], IOEvent | collections.abc.Iterable[IOEvent] | Error | None]
ReadActor = collections.abc.Callable[[Query, ...], IOEvent | collections.abc.Iterable[IOEvent] | Error]
AuditActor = collections.abc.Callable[[Command | Query, ...], Command | Query | Error]
