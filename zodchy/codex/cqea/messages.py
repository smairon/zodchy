import typing
import dataclasses
import collections.abc

Message = dataclasses.make_dataclass('Message', ())
Context = dataclasses.make_dataclass('Context', ())

Query = dataclasses.make_dataclass('Query', (), bases=(Message,))
Command = dataclasses.make_dataclass('Command', (), bases=(Message,))
Event = dataclasses.make_dataclass('Event', (), bases=(Message,))

Error = dataclasses.make_dataclass('Error', (), bases=(Event,))
BDEvent = dataclasses.make_dataclass('BDE', (), bases=(Event,))
IOEvent = dataclasses.make_dataclass('IOE', (), bases=(Event,))

StorageEvent = dataclasses.make_dataclass('StorageEvent', (), bases=(IOEvent,))
ReadEvent = dataclasses.make_dataclass('ReadEvent', (), bases=(StorageEvent,))
WriteEvent = dataclasses.make_dataclass('WriteEvent', (), bases=(StorageEvent,))

ResponseEvent = dataclasses.make_dataclass('ResponseEvent', (), bases=(IOEvent,))

P = typing.TypeVar('P', bound=Query | Command)
C = typing.TypeVar('C', bound=Context)


class Frame(typing.Generic[P, C]):
    payload: P
    context: C


EventStream = collections.abc.Iterable[Event]
