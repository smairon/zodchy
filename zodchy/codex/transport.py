import json
import collections.abc
import typing


T = typing.TypeVar("T")

class CommunicationMessage(typing.Generic[T]):
    def __init__(
        self, 
        id: T, 
        body: collections.abc.Mapping,
        headers: collections.abc.Mapping | None = None
    ):
        self.id = id
        self.body = body
        self.headers = headers
        
    def dump(self, format: typing.Literal["json", "bytes"]) -> str | bytes:    
        result = json.dumps({
            "id": self.id,
            "body": self.body,
            "headers": self.headers,
        })
        if format == "bytes":
            result = result.encode("utf-8")
        return result

class DispatcherContract(typing.Protocol, typing.Generic[T]):
    async def dispatch(self, message: CommunicationMessage[T]) -> bool: ...
    async def shutdown(self) -> None: ...
    
class ReceiverContract(typing.Protocol, typing.Generic[T]):
    async def receive(self) -> typing.AsyncGenerator[CommunicationMessage[T], None]: ...
    async def shutdown(self) -> None: ...