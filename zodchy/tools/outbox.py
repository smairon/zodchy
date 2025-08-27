import abc
import collections.abc
import datetime
import typing

from ..codex.query.bits import FilterBit


T = typing.TypeVar("T")


class OutboxDispatcher:
    __slots__ = ("id", "kind", "settings")

    def __init__(self, kind: str, settings: dict | None = None):
        self.kind = kind
        self.settings = settings

    def __str__(self) -> str:
        return f"Dispatcher(kind={self.kind}, settings={self.settings})"

    def __repr__(self) -> str:
        return self.__str__()


class OutboxEvent:
    __slots__ = ("id", "name", "payload")

    def __init__(self, name: str, payload: dict):
        self.name = name
        self.payload = payload

    def __str__(self) -> str:
        return f"Event(name={self.name}, payload={self.payload})"

    def __repr__(self) -> str:
        return self.__str__()


class OutboxTask:
    __slots__ = ("id", "event", "scheduled_at", "dispatcher")

    def __init__(
        self,
        event: OutboxEvent,
        scheduled_at: datetime.datetime,
        dispatcher: OutboxDispatcher,
    ):
        self.id = id
        self.event = event
        self.scheduled_at = scheduled_at
        self.dispatcher = dispatcher

    def __str__(self) -> str:
        return f"Task(event={self.event}, scheduled_at={self.scheduled_at}, dispatcher={self.dispatcher})"

    def __repr__(self) -> str:
        return self.__str__()


class OutboxClientContract(typing.Protocol[T]):
    async def register_tasks(self, *tasks: OutboxTask) -> list[T]: ...

    async def mark_tasks_as_processed(self, *task_ids: T) -> list[T]: ...

    async def mark_tasks_as_failed(self, *task_ids: T) -> list[T]: ...

    async def mark_tasks_as_cancelled(self, *task_ids: T) -> list[T]: ...

    async def mark_tasks_as_in_progress(self, *task_ids: T) -> list[T]: ...
    
    async def mark_tasks_as_scheduled(self, *task_ids: T, scheduled_at: datetime.datetime) -> list[T]: ...

    async def get_tasks_ready_for_dispatch(
        self, count: int, dispatcher_kind: str | None = None
    ) -> collections.abc.Iterable[OutboxTask]: ...

    async def get_tasks(
        self,
        event_name: FilterBit[str] | None = None,
        dispatcher_kind: FilterBit[str] | None = None,
        status: FilterBit[str] | None = None,
        scheduled_at: FilterBit[datetime.datetime] | None = None,
    ) -> collections.abc.Iterable[OutboxTask]: ...

class OutboxDispatchMessage(abc.ABC):
    payload: dict

    def __init__(self, payload: dict):
        self.payload = payload
        
class OutboxDispatcherContract(typing.Protocol):
    async def dispatch(
        self,
        *messages: OutboxDispatchMessage
    ) -> None: ...