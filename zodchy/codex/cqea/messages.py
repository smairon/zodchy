import abc
import typing
import collections.abc


class Message(abc.ABC):
    pass


class Context(abc.ABC):
    pass


Task = type('Task', (Message, abc.ABC), {})
Event = type('Event', (Message, abc.ABC), {})

Query = type('Query', (Task, abc.ABC), {})
Command = type('Command', (Task, abc.ABC), {})

Error = type('Error', (Event, abc.ABC), {})
BDEvent = type('BDE', (Event, abc.ABC), {})
IOEvent = type('IOE', (Event, abc.ABC), {})

StorageEvent = type('StorageEvent', (IOEvent, abc.ABC), {})
ReadEvent = type('ReadEvent', (StorageEvent, abc.ABC), {})
WriteEvent = type('WriteEvent', (StorageEvent, abc.ABC), {})

ResponseEvent = type('ResponseEvent', (IOEvent, abc.ABC), {})

P = typing.TypeVar('P', bound=Task)
C = typing.TypeVar('C', bound=Context)


class Frame(typing.Generic[P, C]):
    payload: P
    context: C


EventStream = collections.abc.Iterable[Event]
