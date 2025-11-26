from collections.abc import AsyncIterator, Iterator
from typing import Any, Protocol, TypeAlias

from ..codex.cqea import Message

AsyncMessageStreamContract: TypeAlias = AsyncIterator[Message]


class AsyncProcessorContract(Protocol):
    def __call__(
        self,
        stream: AsyncMessageStreamContract,
        *args: Any,
        **kwargs: Any,
    ) -> AsyncMessageStreamContract: ...


class AsyncPipelineContract(Protocol):
    def __call__(self, *messages: Message, **kwargs: Any) -> AsyncMessageStreamContract: ...


class SyncMessageStreamContract(Protocol):
    def __iter__(self) -> Iterator[Message]: ...


class SyncProcessorContract(Protocol):
    def __call__(
        self,
        stream: SyncMessageStreamContract,
        *args: Any,
        **kwargs: Any,
    ) -> SyncMessageStreamContract: ...


class SyncPipelineContract(Protocol):
    def __call__(self, *messages: Message, **kwargs: Any) -> SyncMessageStreamContract: ...
