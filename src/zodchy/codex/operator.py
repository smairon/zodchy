import abc
import collections.abc
import typing

T = typing.TypeVar("T")


class ClauseBit:
    def __init__(self, *data: typing.Self):
        self._data: typing.Any = data

    @property
    def value(self) -> typing.Any:
        return self._data

    def __add__(self, other: typing.Self) -> 'ClauseBit':
        if type(self) is ClauseBit:
            self._data = list(self._data)
            self._data.append(other)
            return self
        else:
            return ClauseBit(self, other)


class SliceBit(ClauseBit):
    def __init__(self, value: int):
        super().__init__()
        self._data: int = value

    @property
    def value(self) -> int:
        return self._data


class FilterBit(abc.ABC, ClauseBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__()
        self._data: T = value

    @property
    def value(self) -> T:
        return self._data

    def __eq__(self, other: typing.Any) -> bool:
        return bool(self._data == other) 


class OrderBit(abc.ABC, ClauseBit):
    def __init__(self, priority: int = 0):
        super().__init__()
        self._data: int = priority

    @property
    def value(self) -> int:
        return self._data


class EQ(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class NE(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class LE(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class GE(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class LT(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class GT(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class IS(FilterBit, typing.Generic[T]):
    def __init__(self, value: T):
        super().__init__(value)


class LIKE(FilterBit, typing.Generic[T]):
    def __init__(self, value: T, case_sensitive: bool = False):
        super().__init__(value)
        self._case_sensitive: bool = case_sensitive

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError
        return self._data == other.value and self._case_sensitive == other.case_sensitive

    @property
    def case_sensitive(self) -> bool:
        return self._case_sensitive


class SET(FilterBit, typing.Generic[T]):
    def __init__(self, *value: T):
        super().__init__(set(value))


class RANGE(FilterBit, typing.Generic[T]):
    def __init__(self, left: GE[T] | GT[T] | None, right: LE[T] | LT[T] | None):
        super().__init__((left, right))


class NOT(FilterBit, typing.Generic[T]):
    def __init__(self, value: EQ[T] | LE[T] | GE[T] | LT[T] | GT[T] | IS[T] | LIKE[T] | SET[T] | RANGE[T]):
        super().__init__(value)
        self._value = value

    def __eq__(self, other: typing.Any) -> bool:
        if hasattr(other, "value"):
            return super().__eq__(other.value)
        else:
            return super().__eq__(other)


class Limit(SliceBit):
    pass


class Offset(SliceBit):
    pass


class ASC(OrderBit):
    pass


class DESC(OrderBit):
    pass


ClauseStream: typing.TypeAlias = collections.abc.Iterable[tuple[str, ClauseBit]]
