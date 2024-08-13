import abc
import typing
import collections.abc


class Message(abc.ABC):
    pass


class Context(abc.ABC):
    pass


class Task(Message, abc.ABC):
    pass


class Event(Message, abc.ABC):
    pass


class Query(Task, abc.ABC):
    pass


class Command(Task, abc.ABC):
    pass


class Error(Event, abc.ABC):
    pass


class BDEvent(Event, abc.ABC):
    pass


class IOEvent(Event, abc.ABC):
    pass


class StorageEvent(IOEvent, abc.ABC):
    pass


class ReadEvent(StorageEvent, abc.ABC):
    pass


class WriteEvent(StorageEvent, abc.ABC):
    pass


class ResponseEvent(IOEvent, abc.ABC):
    pass


P = typing.TypeVar('P', bound=Task)
C = typing.TypeVar('C', bound=Context)


class Frame(typing.Generic[P, C]):
    payload: P
    context: C


EventStream = collections.abc.Iterable[Event]
