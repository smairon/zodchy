"""
Tests for the toolbox.processing module.
"""

import pytest
from typing import AsyncIterator, Iterator
from zodchy.toolbox.processing import (
    AsyncMessageStreamContract,
    AsyncProcessorContract,
    AsyncPipelineContract,
    SyncMessageStreamContract,
    SyncProcessorContract,
    SyncPipelineContract,
)
from zodchy.codex.cqea import Message


class TestAsyncMessageStreamContract:
    """Test class for AsyncMessageStreamContract protocol."""

    def test_async_stream_contract_has_aiter(self):
        """Test that AsyncMessageStreamContract has __aiter__ method."""
        assert hasattr(AsyncMessageStreamContract, "__aiter__")

    async def test_async_stream_implementation(self):
        """Test that a class can implement AsyncMessageStreamContract."""
        class TestMessage(Message):
            def __init__(self, value: str):
                self.value = value

        class SimpleAsyncStream:
            def __init__(self, messages: list[Message]):
                self._messages = messages

            def __aiter__(self) -> AsyncIterator[Message]:
                async def async_gen():
                    for msg in self._messages:
                        yield msg
                return async_gen()

        stream: AsyncMessageStreamContract = SimpleAsyncStream([
            TestMessage("test1"),
            TestMessage("test2"),
        ])
        assert stream is not None

        messages = []
        async for msg in stream:
            messages.append(msg)

        assert len(messages) == 2
        assert messages[0].value == "test1"
        assert messages[1].value == "test2"


class TestAsyncProcessorContract:
    """Test class for AsyncProcessorContract protocol."""

    def test_async_processor_contract_is_callable(self):
        """Test that AsyncProcessorContract is a callable protocol."""
        assert hasattr(AsyncProcessorContract, "__call__")

    async def test_async_processor_implementation(self):
        """Test that a class can implement AsyncProcessorContract."""
        class TestMessage(Message):
            def __init__(self, value: str):
                self.value = value

        class SimpleAsyncProcessor:
            async def __call__(
                self,
                stream: AsyncMessageStreamContract,
                *args,
                **kwargs,
            ) -> AsyncMessageStreamContract:
                class ProcessedStream:
                    def __init__(self, original_stream: AsyncMessageStreamContract):
                        self._stream = original_stream

                    async def __aiter__(self) -> AsyncIterator[Message]:
                        async for msg in self._stream:
                            # Simple transformation: add prefix
                            new_msg = TestMessage(f"processed_{msg.value}")
                            yield new_msg

                return ProcessedStream(stream)

        processor: AsyncProcessorContract = SimpleAsyncProcessor()
        assert processor is not None

        class TestStream:
            def __init__(self, messages: list[Message]):
                self._messages = messages

            async def __aiter__(self) -> AsyncIterator[Message]:
                for msg in self._messages:
                    yield msg

        input_stream: AsyncMessageStreamContract = TestStream([
            TestMessage("test1"),
            TestMessage("test2"),
        ])

        output_stream = await processor(input_stream)
        assert output_stream is not None

        messages = []
        async for msg in output_stream:
            messages.append(msg)

        assert len(messages) == 2
        assert messages[0].value == "processed_test1"
        assert messages[1].value == "processed_test2"


class TestAsyncPipelineContract:
    """Test class for AsyncPipelineContract protocol."""

    def test_async_pipeline_contract_is_callable(self):
        """Test that AsyncPipelineContract is a callable protocol."""
        assert hasattr(AsyncPipelineContract, "__call__")

    async def test_async_pipeline_implementation(self):
        """Test that a class can implement AsyncPipelineContract."""
        class TestMessage(Message):
            def __init__(self, value: str):
                self.value = value

        class SimpleAsyncPipeline:
            async def __call__(self, *messages: Message, **kwargs) -> AsyncMessageStreamContract:
                class PipelineStream:
                    def __init__(self, msgs: tuple[Message, ...]):
                        self._messages = msgs

                    async def __aiter__(self) -> AsyncIterator[Message]:
                        for msg in self._messages:
                            yield msg

                return PipelineStream(messages)

        pipeline: AsyncPipelineContract = SimpleAsyncPipeline()
        assert pipeline is not None

        result_stream = await pipeline(
            TestMessage("msg1"),
            TestMessage("msg2"),
            TestMessage("msg3"),
        )

        messages = []
        async for msg in result_stream:
            messages.append(msg)

        assert len(messages) == 3
        assert messages[0].value == "msg1"
        assert messages[1].value == "msg2"
        assert messages[2].value == "msg3"


class TestSyncMessageStreamContract:
    """Test class for SyncMessageStreamContract protocol."""

    def test_sync_stream_contract_has_iter(self):
        """Test that SyncMessageStreamContract has __iter__ method."""
        assert hasattr(SyncMessageStreamContract, "__iter__")

    def test_sync_stream_implementation(self):
        """Test that a class can implement SyncMessageStreamContract."""
        class TestMessage(Message):
            def __init__(self, value: str):
                self.value = value

        class SimpleSyncStream:
            def __init__(self, messages: list[Message]):
                self._messages = messages

            def __iter__(self) -> Iterator[Message]:
                return iter(self._messages)

        stream: SyncMessageStreamContract = SimpleSyncStream([
            TestMessage("test1"),
            TestMessage("test2"),
        ])
        assert stream is not None

        messages = list(stream)
        assert len(messages) == 2
        assert messages[0].value == "test1"
        assert messages[1].value == "test2"


class TestSyncProcessorContract:
    """Test class for SyncProcessorContract protocol."""

    def test_sync_processor_contract_is_callable(self):
        """Test that SyncProcessorContract is a callable protocol."""
        assert hasattr(SyncProcessorContract, "__call__")

    def test_sync_processor_implementation(self):
        """Test that a class can implement SyncProcessorContract."""
        class TestMessage(Message):
            def __init__(self, value: str):
                self.value = value

        class SimpleSyncProcessor:
            def __call__(
                self,
                stream: SyncMessageStreamContract,
                *args,
                **kwargs,
            ) -> SyncMessageStreamContract:
                class ProcessedStream:
                    def __init__(self, original_stream: SyncMessageStreamContract):
                        self._stream = original_stream

                    def __iter__(self) -> Iterator[Message]:
                        for msg in self._stream:
                            # Simple transformation: add prefix
                            new_msg = TestMessage(f"processed_{msg.value}")
                            yield new_msg

                return ProcessedStream(stream)

        processor: SyncProcessorContract = SimpleSyncProcessor()
        assert processor is not None

        class TestStream:
            def __init__(self, messages: list[Message]):
                self._messages = messages

            def __iter__(self) -> Iterator[Message]:
                return iter(self._messages)

        input_stream: SyncMessageStreamContract = TestStream([
            TestMessage("test1"),
            TestMessage("test2"),
        ])

        output_stream = processor(input_stream)
        assert output_stream is not None

        messages = list(output_stream)
        assert len(messages) == 2
        assert messages[0].value == "processed_test1"
        assert messages[1].value == "processed_test2"


class TestSyncPipelineContract:
    """Test class for SyncPipelineContract protocol."""

    def test_sync_pipeline_contract_is_callable(self):
        """Test that SyncPipelineContract is a callable protocol."""
        assert hasattr(SyncPipelineContract, "__call__")

    def test_sync_pipeline_implementation(self):
        """Test that a class can implement SyncPipelineContract."""
        class TestMessage(Message):
            def __init__(self, value: str):
                self.value = value

        class SimpleSyncPipeline:
            def __call__(self, *messages: Message, **kwargs) -> SyncMessageStreamContract:
                class PipelineStream:
                    def __init__(self, msgs: tuple[Message, ...]):
                        self._messages = msgs

                    def __iter__(self) -> Iterator[Message]:
                        return iter(self._messages)

                return PipelineStream(messages)

        pipeline: SyncPipelineContract = SimpleSyncPipeline()
        assert pipeline is not None

        result_stream = pipeline(
            TestMessage("msg1"),
            TestMessage("msg2"),
            TestMessage("msg3"),
        )

        messages = list(result_stream)
        assert len(messages) == 3
        assert messages[0].value == "msg1"
        assert messages[1].value == "msg2"
        assert messages[2].value == "msg3"


class TestProcessingContractsIntegration:
    """Test class for integration of processing contracts."""

    async def test_async_pipeline_with_processor(self):
        """Test async pipeline with processor integration."""
        class TestMessage(Message):
            def __init__(self, value: str):
                self.value = value

        class AsyncProcessor:
            async def __call__(
                self,
                stream: AsyncMessageStreamContract,
                *args,
                **kwargs,
            ) -> AsyncMessageStreamContract:
                class ProcessedStream:
                    def __init__(self, original: AsyncMessageStreamContract):
                        self._original = original

                    async def __aiter__(self) -> AsyncIterator[Message]:
                        async for msg in self._original:
                            yield TestMessage(f"processed_{msg.value}")

                return ProcessedStream(stream)

        class AsyncPipeline:
            async def __call__(self, *messages: Message, **kwargs) -> AsyncMessageStreamContract:
                processor = AsyncProcessor()

                class InputStream:
                    def __init__(self, msgs: tuple[Message, ...]):
                        self._msgs = msgs

                    async def __aiter__(self) -> AsyncIterator[Message]:
                        for msg in self._msgs:
                            yield msg

                input_stream = InputStream(messages)
                return await processor(input_stream)

        pipeline: AsyncPipelineContract = AsyncPipeline()
        result = await pipeline(TestMessage("test"))

        messages = []
        async for msg in result:
            messages.append(msg)

        assert len(messages) == 1
        assert messages[0].value == "processed_test"

    def test_sync_pipeline_with_processor(self):
        """Test sync pipeline with processor integration."""
        class TestMessage(Message):
            def __init__(self, value: str):
                self.value = value

        class SyncProcessor:
            def __call__(
                self,
                stream: SyncMessageStreamContract,
                *args,
                **kwargs,
            ) -> SyncMessageStreamContract:
                class ProcessedStream:
                    def __init__(self, original: SyncMessageStreamContract):
                        self._original = original

                    def __iter__(self) -> Iterator[Message]:
                        for msg in self._original:
                            yield TestMessage(f"processed_{msg.value}")

                return ProcessedStream(stream)

        class SyncPipeline:
            def __call__(self, *messages: Message, **kwargs) -> SyncMessageStreamContract:
                processor = SyncProcessor()

                class InputStream:
                    def __init__(self, msgs: tuple[Message, ...]):
                        self._msgs = msgs

                    def __iter__(self) -> Iterator[Message]:
                        return iter(self._msgs)

                input_stream = InputStream(messages)
                return processor(input_stream)

        pipeline: SyncPipelineContract = SyncPipeline()
        result = pipeline(TestMessage("test"))

        messages = list(result)
        assert len(messages) == 1
        assert messages[0].value == "processed_test"

