from collections.abc import AsyncIterator, Iterator
from typing import Any, Protocol

from ..codex.cqea import Message


class AsyncMessageStreamContract(Protocol):
    def __aiter__(self) -> AsyncIterator[Message]: ...


class AsyncProcessorContract(Protocol):
    async def __call__(
        self,
        stream: AsyncMessageStreamContract,
        *args,
        **kwargs,
    ) -> AsyncMessageStreamContract: ...


class AsyncPipelineContract(Protocol):
    async def __call__(self, *messages: Message, **kwargs: Any) -> AsyncMessageStreamContract: ...


class SyncMessageStreamContract(Protocol):
    def __iter__(self) -> Iterator[Message]: ...


class SyncProcessorContract(Protocol):
    def __call__(
        self,
        stream: SyncMessageStreamContract,
        *args,
        **kwargs,
    ) -> SyncMessageStreamContract: ...


class SyncPipelineContract(Protocol):
    def __call__(self, *messages: Message, **kwargs: Any) -> SyncMessageStreamContract: ...
