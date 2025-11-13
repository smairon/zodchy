import abc
import collections.abc
import typing
from .operator import ClauseStream


class Message(abc.ABC):
    pass


class Context(abc.ABC):
    pass


class Task(Message, abc.ABC):
    pass


class Command(Task, abc.ABC):
    pass


class Event(Message, abc.ABC):
    pass


class Error(Event, abc.ABC):
    pass


class Query(Task, abc.ABC):
    @abc.abstractmethod
    def __iter__(self) -> ClauseStream: ...


class View(Event, abc.ABC):
    @abc.abstractmethod
    def data(self) -> typing.Any: ...

    def meta(self) -> collections.abc.Mapping[str, typing.Any] | None:
        pass
