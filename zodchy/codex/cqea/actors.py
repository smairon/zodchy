import collections.abc
import typing

from .messages import (
    Message
)

P = typing.ParamSpec('P')

Actor = collections.abc.Callable[
    typing.Concatenate[Message, P],
    Message | collections.abc.Iterable[Message] | None
]
