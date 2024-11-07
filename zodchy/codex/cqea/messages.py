import abc
import collections.abc

from ..query.bits import ClauseBit


class Message(abc.ABC):
    pass


class Context(Message, abc.ABC):
    pass


class Task(Message, abc.ABC):
    pass


class Event(Message, abc.ABC):
    pass


class Query(Task, abc.ABC):
    @abc.abstractmethod
    def __iter__(self) -> collections.abc.Iterable[tuple[str, ClauseBit]]: ...


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


EventStream = collections.abc.Iterable[Event]
